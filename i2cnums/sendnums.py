import sys
import piToNixie

if len(sys.argv) > 1:
  piToNixie.sendNum(int(sys.argv[1]), 0)
if len(sys.argv) > 2:
  piToNixie.sendBrightness(int(sys.argv[2]))
if len(sys.argv) > 3:
  piToNixie.sendNum(int(sys.argv[3]), 1)
if len(sys.argv) > 4:
  piToNixie.sendBrightness(int(sys.argv[4]))
if len(sys.argv) > 5:
  piToNixie.sendNum(int(sys.argv[5]), 2)
if len(sys.argv) > 6:
  piToNixie.sendBrightness(int(sys.argv[6]))
if len(sys.argv) > 7:
  piToNixie.sendNum(int(sys.argv[7]), 3)
if len(sys.argv) > 8:
  piToNixie.sendBrightness(int(sys.argv[8]))
piToNixie.sendEnd()
