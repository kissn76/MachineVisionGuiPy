import cv2


ImreadModes = {
    "IMREAD_UNCHANGED": cv2.IMREAD_UNCHANGED,
    "IMREAD_GRAYSCALE": cv2.IMREAD_GRAYSCALE,
    "IMREAD_COLOR": cv2.IMREAD_COLOR,
    "IMREAD_ANYDEPTH": cv2.IMREAD_ANYDEPTH,
    "IMREAD_ANYCOLOR": cv2.IMREAD_ANYCOLOR,
    "IMREAD_LOAD_GDAL": cv2.IMREAD_LOAD_GDAL,
    "IMREAD_REDUCED_GRAYSCALE_2": cv2.IMREAD_REDUCED_GRAYSCALE_2,
    "IMREAD_REDUCED_COLOR_2": cv2.IMREAD_REDUCED_COLOR_2,
    "IMREAD_REDUCED_GRAYSCALE_4": cv2.IMREAD_REDUCED_GRAYSCALE_4,
    "IMREAD_REDUCED_COLOR_4": cv2.IMREAD_REDUCED_COLOR_4,
    "IMREAD_REDUCED_GRAYSCALE_8": cv2.IMREAD_REDUCED_GRAYSCALE_8,
    "IMREAD_REDUCED_COLOR_8": cv2.IMREAD_REDUCED_COLOR_8,
    "IMREAD_IGNORE_ORIENTATION": cv2.IMREAD_IGNORE_ORIENTATION
}

ImwriteEXRCompressionFlags = {
    "IMWRITE_EXR_COMPRESSION_NO": cv2.IMWRITE_EXR_COMPRESSION_NO,
    "IMWRITE_EXR_COMPRESSION_RLE": cv2.IMWRITE_EXR_COMPRESSION_RLE,
    "IMWRITE_EXR_COMPRESSION_ZIPS": cv2.IMWRITE_EXR_COMPRESSION_ZIPS,
    "IMWRITE_EXR_COMPRESSION_ZIP": cv2.IMWRITE_EXR_COMPRESSION_ZIP,
    "IMWRITE_EXR_COMPRESSION_PIZ": cv2.IMWRITE_EXR_COMPRESSION_PIZ,
    "IMWRITE_EXR_COMPRESSION_PXR24": cv2.IMWRITE_EXR_COMPRESSION_PXR24,
    "IMWRITE_EXR_COMPRESSION_B44": cv2.IMWRITE_EXR_COMPRESSION_B44,
    "IMWRITE_EXR_COMPRESSION_B44A": cv2.IMWRITE_EXR_COMPRESSION_B44A,
    "IMWRITE_EXR_COMPRESSION_DWAA": cv2.IMWRITE_EXR_COMPRESSION_DWAA,
    "IMWRITE_EXR_COMPRESSION_DWAB": cv2.IMWRITE_EXR_COMPRESSION_DWAB
}

ImwriteEXRTypeFlags = {
    "IMWRITE_EXR_TYPE_HALF": cv2.IMWRITE_EXR_TYPE_HALF,
    "IMWRITE_EXR_TYPE_FLOAT": cv2.IMWRITE_EXR_TYPE_FLOAT
}

ImwriteFlags = {
    "IMWRITE_JPEG_QUALITY": cv2.IMWRITE_JPEG_QUALITY,
    "IMWRITE_JPEG_PROGRESSIVE": cv2.IMWRITE_JPEG_PROGRESSIVE,
    "IMWRITE_JPEG_OPTIMIZE": cv2.IMWRITE_JPEG_OPTIMIZE,
    "IMWRITE_JPEG_RST_INTERVAL": cv2.IMWRITE_JPEG_RST_INTERVAL,
    "IMWRITE_JPEG_LUMA_QUALITY": cv2.IMWRITE_JPEG_LUMA_QUALITY,
    "IMWRITE_JPEG_CHROMA_QUALITY": cv2.IMWRITE_JPEG_CHROMA_QUALITY,
    "IMWRITE_JPEG_SAMPLING_FACTOR": cv2.IMWRITE_JPEG_SAMPLING_FACTOR,
    "IMWRITE_PNG_COMPRESSION": cv2.IMWRITE_PNG_COMPRESSION,
    "IMWRITE_PNG_STRATEGY": cv2.IMWRITE_PNG_STRATEGY,
    "IMWRITE_PNG_BILEVEL": cv2.IMWRITE_PNG_BILEVEL,
    "IMWRITE_PXM_BINARY": cv2.IMWRITE_PXM_BINARY,
    "IMWRITE_EXR_TYPE": cv2.IMWRITE_EXR_TYPE,
    "IMWRITE_EXR_COMPRESSION": cv2.IMWRITE_EXR_COMPRESSION,
    "IMWRITE_EXR_DWA_COMPRESSION_LEVEL": cv2.IMWRITE_EXR_DWA_COMPRESSION_LEVEL,
    "IMWRITE_WEBP_QUALITY": cv2.IMWRITE_WEBP_QUALITY,
    "IMWRITE_HDR_COMPRESSION": cv2.IMWRITE_HDR_COMPRESSION,
    "IMWRITE_PAM_TUPLETYPE": cv2.IMWRITE_PAM_TUPLETYPE,
    "IMWRITE_TIFF_RESUNIT": cv2.IMWRITE_TIFF_RESUNIT,
    "IMWRITE_TIFF_XDPI": cv2.IMWRITE_TIFF_XDPI,
    "IMWRITE_TIFF_YDPI": cv2.IMWRITE_TIFF_YDPI,
    "IMWRITE_TIFF_COMPRESSION": cv2.IMWRITE_TIFF_COMPRESSION,
    "IMWRITE_JPEG2000_COMPRESSION_X1000": cv2.IMWRITE_JPEG2000_COMPRESSION_X1000
}

ImwriteHDRCompressionFlags = {
    "IMWRITE_HDR_COMPRESSION_NONE": cv2.IMWRITE_HDR_COMPRESSION_NONE,
    "IMWRITE_HDR_COMPRESSION_RLE": cv2.IMWRITE_HDR_COMPRESSION_RLE
}

ImwriteJPEGSamplingFactorParams = {
    "IMWRITE_JPEG_SAMPLING_FACTOR_411": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_411,
    "IMWRITE_JPEG_SAMPLING_FACTOR_420": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_420,
    "IMWRITE_JPEG_SAMPLING_FACTOR_422": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_422,
    "IMWRITE_JPEG_SAMPLING_FACTOR_440": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_440,
    "IMWRITE_JPEG_SAMPLING_FACTOR_444": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444
}

ImwritePAMFlags = {
    "IMWRITE_PAM_FORMAT_NULL": cv2.IMWRITE_PAM_FORMAT_NULL,
    "IMWRITE_PAM_FORMAT_BLACKANDWHITE": cv2.IMWRITE_PAM_FORMAT_BLACKANDWHITE,
    "IMWRITE_PAM_FORMAT_GRAYSCALE": cv2.IMWRITE_PAM_FORMAT_GRAYSCALE,
    "IMWRITE_PAM_FORMAT_GRAYSCALE_ALPHA": cv2.IMWRITE_PAM_FORMAT_GRAYSCALE_ALPHA,
    "IMWRITE_PAM_FORMAT_RGB": cv2.IMWRITE_PAM_FORMAT_RGB,
    "IMWRITE_PAM_FORMAT_RGB_ALPHA": cv2.IMWRITE_PAM_FORMAT_RGB_ALPHA
}

ImwritePNGFlags = {
    "IMWRITE_PNG_STRATEGY_DEFAULT": cv2.IMWRITE_PNG_STRATEGY_DEFAULT,
    "IMWRITE_PNG_STRATEGY_FILTERED": cv2.IMWRITE_PNG_STRATEGY_FILTERED,
    "IMWRITE_PNG_STRATEGY_HUFFMAN_ONLY": cv2.IMWRITE_PNG_STRATEGY_HUFFMAN_ONLY,
    "IMWRITE_PNG_STRATEGY_RLE": cv2.IMWRITE_PNG_STRATEGY_RLE,
    "IMWRITE_PNG_STRATEGY_FIXED": cv2.IMWRITE_PNG_STRATEGY_FIXED
}
