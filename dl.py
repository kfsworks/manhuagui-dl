
import os
import json
import requests
from PIL import Image

# https:// i.hamreus.com/ps2/0-9/7jingang_wy3qy/01/seemh-001-a3d0.JPG?cid=246197&md5=WDl0h-vggXtaIXp099AuKQ
# curl  -e "https://tw.manhuagui.com/" "https://i.hamreus.com/ps2/0-9/7jingang_wy3qy/22/seemh-101-e5f6.jpg?cid=246218&md5=K9BZ0c5TmDJfEZ716LWpUw" -o a.jpg

def process(url, savefilename, headerstr):
  r = requests.get(url, stream=True, headers={'Referer': headerstr})
  r.raise_for_status()
  r.raw.decode_content = True  # Required to decompress gzip/deflate compressed responses.
  with Image.open(r.raw) as img:
    img.save(savefilename)
  r.close()


host = 'i.hamreus.com'
header = "https://tw.manhuagui.com/"
srcpath = os.getcwd() + '/data'
destpath = os.getcwd() + '/dest'
srcfolder = os.fsencode(srcpath)
for file in os.listdir(srcfolder):
  filename = srcpath + '/' + os.fsdecode(file)
  with open(filename, "r") as fd:
    src = json.load(fd)
    for n in src['files']:
      n = n[:n.find('.webp')]
      url = 'https://{}{}{}?cid={}&md5={}'.format(host, src['path'],n, src['cid'], src['sl']['md5'])
      savename = '{}/{}-{}-{}'.format(destpath, src['bname'], src['cname'], n)
      process(url, savename, header)
