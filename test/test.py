import sys
import pds4_tools
import numpy as np

from PIL import Image
import colour
import colour_demosaicing
from skimage import exposure

# 读入pds label
pds_data = pds4_tools.read('CE4_GRAS_PCAML-C-000_SCI_N_20190104041518_20190104041518_0001_B.2BL')

# pds4-tools自带的浏览器
#pds4_tools.view(from_existing_structures=pds_data)

# 将图像数据提取出来
raw_data = np.asanyarray(pds_data[0].data)
print(raw_data.shape, raw_data.ndim)
raw_data = raw_data / 1023      #10位的图像数据归一化 

# de-bayer
rgb_data = colour.cctf_encoding(colour_demosaicing.demosaicing_CFA_Bayer_bilinear(raw_data, 'RGGB')) 
print(rgb_data.shape, rgb_data.ndim)

# 直方图拉伸
lower, upper = np.percentile(rgb_data, (0.2,99.8))
print(lower, upper)
scale_data = exposure.rescale_intensity(rgb_data, in_range=(lower, upper)) 

#[h, w] = data.shape
#m = np.max(data)
#f = 256/m
#
#ndata = np.empty([h, w , 3], dtype = np.uint8) 
#print(ndata.shape, ndata.ndim, m, f)
#
##for y in range(h):
##    for x in range(w):
##        #p1 = ((data[y, x] & 63488) >> 11) * 8
##        #p2 = ((data[y,x] & 2016) >> 5) * 4
##        #p3 = data[y,x] & 31 * 8
##        p1 = data[y, x]*256/m
##        p2 = data[y, x]*256/m
##        p3 = data[y, x]*256/m
##        ndata[y,x,:] = [p1, p2, p3]
#
#ndata[:,:,0] = data*f
#ndata[:,:,1] = data*f
#ndata[:,:,2] = data*f

#im = Image.fromarray(ndata.astype('uint8'))
#im = Image.fromarray(data.astype('uint8'))

# 保存原始图像
raw_data = raw_data*255 # 放大到8位
im0 = Image.fromarray(raw_data.astype('uint8'))
im0.save('./test0.png')   #保存图片

# 保存debayer之后的彩色图像
rgb_data = rgb_data*255 # 放大到8位
im1 = Image.fromarray(rgb_data.astype('uint8'))
im1.save('./test1.png')   #保存图片

# 保存直方图拉伸之后的彩色图像
scale_data = scale_data*255
im2 = Image.fromarray(scale_data.astype('uint8'))
im2.save('./test2.png')   #保存图片






