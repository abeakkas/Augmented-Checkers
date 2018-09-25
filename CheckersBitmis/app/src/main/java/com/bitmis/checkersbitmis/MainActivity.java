package com.bitmis.checkersbitmis;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.PixelFormat;
import android.graphics.PorterDuff;
import android.graphics.SurfaceTexture;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CameraMetadata;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.util.Size;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.TextureView;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity implements SurfaceHolder.Callback {
    private static final String TAG = "AndroidCameraApi";

    private TextureView textureView;
    private String cameraId;
    protected CameraDevice cameraDevice;
    protected CaptureRequest.Builder captureRequestBuilder;
    private Size imageDimension;
    private static final int REQUEST_CAMERA_PERMISSION = 200;
    private Handler mSendHandler;
    private Handler mPreviewHandler;

    private SurfaceView surfaceView;
    private SurfaceHolder surfaceHolder;
    private int[][] pts = new int[100][2];
    int ptsN = 0;
    int pixSc = 4;
    private int[][][] centers = new int[8][8][2];
    private int[][][] corners = new int[9][9][2];
    private int[][] moves = new int[100][2];
    private int moveLen = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textureView = (TextureView) findViewById(R.id.texture);
        textureView.setSurfaceTextureListener(textureListener);
        startBackgroundThread();
        surfaceView = (SurfaceView) findViewById(R.id.surface);
        surfaceView.setZOrderOnTop(true);
        surfaceHolder = surfaceView.getHolder();
        surfaceHolder.addCallback(this);
        surfaceHolder.setFormat(PixelFormat.TRANSPARENT);
    }

    TextureView.SurfaceTextureListener textureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
            openCamera();
        }

        @Override
        public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {
        }

        @Override
        public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
            return false;
        }

        @Override
        public void onSurfaceTextureUpdated(SurfaceTexture surface) {
        }
    };

    private final CameraDevice.StateCallback stateCallback = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(CameraDevice camera) {
            //This is called when the camera is open
            Log.e(TAG, "onOpened");
            cameraDevice = camera;
            createCameraPreview();
        }

        @Override
        public void onDisconnected(CameraDevice camera) {
            cameraDevice.close();
        }

        @Override
        public void onError(CameraDevice camera, int error) {
            cameraDevice.close();
            cameraDevice = null;
        }
    };

    protected void startBackgroundThread() {
        HandlerThread sendThread = new HandlerThread("Send Thread");
        sendThread.start();
        mSendHandler = new Handler(sendThread.getLooper());
        HandlerThread previewThread = new HandlerThread("Preview Thread");
        previewThread.start();
        mPreviewHandler = new Handler(previewThread.getLooper());
    }

    protected void takePicture() {
        mSendHandler.post(new Runnable() {
            @Override
            public void run() {
                Bitmap x = textureView.getBitmap();
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                Bitmap.createScaledBitmap(x, x.getWidth() / pixSc, x.getHeight() / pixSc, false).compress(Bitmap.CompressFormat.JPEG, 90, out);
                byte[] bytes = out.toByteArray();
                HttpClient client = new DefaultHttpClient();
                HttpPost post = new HttpPost("http://192.168.43.29:8000");
                post.setEntity(new ByteArrayEntity(bytes));
                post.setHeader("Content-type", "image/jpeg");
                HttpResponse response = null;
                try {
                    response = client.execute(post);
                    String restext = convertInputStreamToString(response.getEntity().getContent());
                    Log.d("mustafa", "" + restext);
                    if (restext != null && !restext.equals("")) {
                        String[] sp = restext.split("-");
                        if (sp.length < 2) {
                            moveLen = 0;
                            return;
                        }
                        int ctr = 0;
                        if (sp.length >= 9 * 9 * 2) {
                            for (int i = 0; i < 9; i++) {
                                for (int j = 0; j < 9; j++) {
                                    corners[i][j][0] = Integer.parseInt(sp[ctr++]) * pixSc;
                                    corners[i][j][1] = Integer.parseInt(sp[ctr++]) * pixSc;
                                }
                            }
                        }
                        if (sp.length >= 8 * 8 * 2) {
                            for (int i = 0; i < 8; i++) {
                                for (int j = 0; j < 8; j++) {
                                    centers[i][j][0] = Integer.parseInt(sp[ctr++]) * pixSc;
                                    centers[i][j][1] = Integer.parseInt(sp[ctr++]) * pixSc;
                                }
                            }
                        }
                        moveLen = Integer.parseInt(sp[ctr++]);
                        for (int i = 0; i < moveLen; i++) {
                            moves[i][1] = Integer.parseInt(sp[ctr++]);
                            moves[i][0] = Integer.parseInt(sp[ctr++]);
                        }
                    } else {
                        moveLen = 0;
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                } finally {
                    takePicture();
                }
            }
        });
    }

    protected void createCameraPreview() {
        try {
            SurfaceTexture texture = textureView.getSurfaceTexture();
            texture.setDefaultBufferSize(imageDimension.getWidth(), imageDimension.getHeight());
            Surface surface = new Surface(texture);
            captureRequestBuilder = cameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);
            captureRequestBuilder.addTarget(surface);
            cameraDevice.createCaptureSession(Arrays.asList(surface), new CameraCaptureSession.StateCallback() {
                @Override
                public void onConfigured(@NonNull CameraCaptureSession session) {
                    //The camera is already closed
                    if (null == cameraDevice) {
                        return;
                    }
                    captureRequestBuilder.set(CaptureRequest.CONTROL_MODE, CameraMetadata.CONTROL_MODE_AUTO);
                    try {
                        session.setRepeatingRequest(captureRequestBuilder.build(), null, mPreviewHandler);
                        takePicture();
                    } catch (CameraAccessException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onConfigureFailed(@NonNull CameraCaptureSession cameraCaptureSession) {
                }
            }, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
    }

    private void openCamera() {
        CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
        Log.e(TAG, "is camera open");
        try {
            cameraId = manager.getCameraIdList()[0];
            CameraCharacteristics characteristics = manager.getCameraCharacteristics(cameraId);
            StreamConfigurationMap map = characteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
            assert map != null;
            imageDimension = map.getOutputSizes(SurfaceTexture.class)[0];
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE}, REQUEST_CAMERA_PERMISSION);
                return;
            }
            manager.openCamera(cameraId, stateCallback, null);
        } catch (CameraAccessException e) {
            e.printStackTrace();
        }
        Log.e(TAG, "openCamera X");
    }

    private static String convertInputStreamToString(InputStream inputStream) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        String line = "";
        String result = "";
        while ((line = bufferedReader.readLine()) != null) {
            result += line;
        }
        inputStream.close();
        return result;

    }

    private void startDrawing() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Canvas canvas = surfaceHolder.lockCanvas();
                            canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR);
                            Paint p = new Paint();
                            float x = System.currentTimeMillis() % 1500 / 1500f;
                            p.setPathEffect(new DashPathEffect(new float[]{20, 20}, -x * 40));
                            p.setColor(Color.RED);
                            p.setStrokeWidth(12);
                            Paint p2 = new Paint();
                            p2.setColor(Color.RED);
                            p2.setStrokeWidth(8);
                            Paint p3 = new Paint();
                            p3.setColor(Color.GREEN);
                            p3.setStyle(Paint.Style.STROKE);
                            p3.setStrokeWidth(2);
                            if (moveLen > 0) {
                                for (int i = 0; i < moveLen; i++) {
                                    if (i < moveLen - 1) {
                                        int l = 30;
                                        int x1 = centers[moves[i][0]][moves[i][1]][0];
                                        int y1 = centers[moves[i][0]][moves[i][1]][1];
                                        int x2 = centers[moves[i + 1][0]][moves[i + 1][1]][0];
                                        int y2 = centers[moves[i + 1][0]][moves[i + 1][1]][1];
                                        int dx = (int)(l * (x1 - x2) / Math.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)));
                                        int dy = (int)(l * (y1 - y2) / Math.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2)));
                                        Path path = new Path();
                                        path.moveTo(corners[moves[i + 1][0]][moves[i + 1][1]][0], corners[moves[i + 1][0]][moves[i + 1][1]][1]);
                                        path.lineTo(corners[moves[i + 1][0] + 1][moves[i + 1][1]][0], corners[moves[i + 1][0] + 1][moves[i + 1][1]][1]);
                                        path.lineTo(corners[moves[i + 1][0] + 1][moves[i + 1][1] + 1][0], corners[moves[i + 1][0] + 1][moves[i + 1][1] + 1][1]);
                                        path.lineTo(corners[moves[i + 1][0]][moves[i + 1][1] + 1][0], corners[moves[i + 1][0]][moves[i + 1][1] + 1][1]);
                                        path.close();
                                        if (i == moveLen - 2) {
                                            p3.setStrokeWidth(5);
                                        }
                                        canvas.drawPath(path, p3);
                                        canvas.drawLine(
                                                x1 - dx / 2,
                                                y1 - dy / 2,
                                                x2 + dx / 2,
                                                y2 + dy / 2,
                                                p);
                                        float c = .7f;
                                        // Old
                                        /*
                                        canvas.drawLine(
                                                x2 + dx + (int)(dy * c),
                                                y2 + dy - (int)(dx * c),
                                                x2,
                                                y2,
                                                p2);
                                        canvas.drawLine(
                                                x2 + dx - (int)(dy * c),
                                                y2 + dy + (int)(dx * c),
                                                x2,
                                                y2,
                                                p2);
                                                */
                                        // New
                                        path = new Path();
                                        path.moveTo(x2, y2);
                                        path.lineTo(x2 + dx + (int)(dy * c), y2 + dy - (int)(dx * c));
                                        path.lineTo(x2 + dx - (int)(dy * c), y2 + dy + (int)(dx * c));
                                        path.close();
                                        canvas.drawPath(path, p2);
                                    }
                                }
                            }
                            surfaceHolder.unlockCanvasAndPost(canvas);
                        }
                    });
                    try {
                        Thread.sleep(40);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

    @Override
    public void surfaceCreated(SurfaceHolder surfaceHolder) {
        startDrawing();
    }

    @Override
    public void surfaceChanged(SurfaceHolder surfaceHolder, int i, int i1, int i2) {
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder surfaceHolder) {
    }
}
