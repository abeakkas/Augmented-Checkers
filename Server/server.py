import io
import http.server
import socketserver
import atexit
import sys
import logic
import numpy as np
from time import time
from PIL import Image

from Vision import get_corners

class Handler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        return

    def do_POST(self):
        start = time()
        self._set_headers()
        content_len = int(self.headers['Content-Length'])
        print("Content Length: {}".format(content_len))
        post_body = self.rfile.read(content_len)
        img = Image.open(io.BytesIO(post_body))
        corners, matris, centers = get_corners(img)
        print("Took {} seconds!".format(time() - start))
        if corners is None:
            self.wfile.write(b"")
            return
        response = ""
        for i in range(9):
            for j in range(9):
                response += str(int(corners[i][j][0])) + "-"
                response += str(int(corners[i][j][1])) + "-"
        # self.wfile.write(response.encode())
        # response = ""
        for i in range(8):
            for j in range(8):
                response += str(int(centers[i,j,0])) + "-"
                response += str(int(centers[i,j,1])) + "-"
        t = time()
        # best_move_nusret = logic.calc_best_move(matris.astype(np.int8), 1)
        moves = logic.give_moves(matris.astype(np.int8), 1)
        best_move = moves[0]
        for m in moves:
            if len(m) > len(best_move):
                best_move = m
        # best_move = best_move_nusret # TODO: sil
        best_move2 = [best_move[-1]]
        if len(best_move) != 3:
            for i in range(len(best_move) - 3):
                best_move2.append([
                    2 * best_move[len(best_move) - 3 - i][0] - best_move2[-1][0],
                    2 * best_move[len(best_move) - 3 - i][1] - best_move2[-1][1]])
        else:
            best_move2.append(best_move[0])
        print(time() - t)
        response += str(len(best_move2)) + "-"
        for i in range(len(best_move2)):
            response += str(best_move2[i][0]) + "-"
            response += str(best_move2[i][1]) + "-"
        response += "0-"
        self.wfile.write(response.encode())

print('Server listening on port 8000...')
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('', int(sys.argv[1])), Handler)
atexit.register(httpd.server_close)
httpd.serve_forever()
