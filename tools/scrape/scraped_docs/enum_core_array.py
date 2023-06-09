import cv2


BorderTypes = {
    "BORDER_CONSTANT": cv2.BORDER_CONSTANT,
    "BORDER_REPLICATE": cv2.BORDER_REPLICATE,
    "BORDER_REFLECT": cv2.BORDER_REFLECT,
    "BORDER_WRAP": cv2.BORDER_WRAP,
    "BORDER_REFLECT_101": cv2.BORDER_REFLECT_101,
    "BORDER_TRANSPARENT": cv2.BORDER_TRANSPARENT,
    "BORDER_REFLECT101": cv2.BORDER_REFLECT101,
    "BORDER_DEFAULT": cv2.BORDER_DEFAULT,
    "BORDER_ISOLATED": cv2.BORDER_ISOLATED
}

CmpTypes = {
    "CMP_EQ": cv2.CMP_EQ,
    "CMP_GT": cv2.CMP_GT,
    "CMP_GE": cv2.CMP_GE,
    "CMP_LT": cv2.CMP_LT,
    "CMP_LE": cv2.CMP_LE,
    "CMP_NE": cv2.CMP_NE
}

DecompTypes = {
    "DECOMP_LU": cv2.DECOMP_LU,
    "DECOMP_SVD": cv2.DECOMP_SVD,
    "DECOMP_EIG": cv2.DECOMP_EIG,
    "DECOMP_CHOLESKY": cv2.DECOMP_CHOLESKY,
    "DECOMP_QR": cv2.DECOMP_QR,
    "DECOMP_NORMAL": cv2.DECOMP_NORMAL
}

DftFlags = {
    "DFT_INVERSE": cv2.DFT_INVERSE,
    "DFT_SCALE": cv2.DFT_SCALE,
    "DFT_ROWS": cv2.DFT_ROWS,
    "DFT_COMPLEX_OUTPUT": cv2.DFT_COMPLEX_OUTPUT,
    "DFT_REAL_OUTPUT": cv2.DFT_REAL_OUTPUT,
    "DFT_COMPLEX_INPUT": cv2.DFT_COMPLEX_INPUT,
    "DCT_INVERSE": cv2.DCT_INVERSE,
    "DCT_ROWS": cv2.DCT_ROWS
}

GemmFlags = {
    "GEMM_1_T": cv2.GEMM_1_T,
    "GEMM_2_T": cv2.GEMM_2_T,
    "GEMM_3_T": cv2.GEMM_3_T
}

NormTypes = {
    "NORM_INF": cv2.NORM_INF,
    "NORM_L1": cv2.NORM_L1,
    "NORM_L2": cv2.NORM_L2,
    "NORM_L2SQR": cv2.NORM_L2SQR,
    "NORM_HAMMING": cv2.NORM_HAMMING,
    "NORM_HAMMING2": cv2.NORM_HAMMING2,
    "NORM_TYPE_MASK": cv2.NORM_TYPE_MASK,
    "NORM_RELATIVE": cv2.NORM_RELATIVE,
    "NORM_MINMAX": cv2.NORM_MINMAX
}

ReduceTypes = {
    "REDUCE_SUM": cv2.REDUCE_SUM,
    "REDUCE_AVG": cv2.REDUCE_AVG,
    "REDUCE_MAX": cv2.REDUCE_MAX,
    "REDUCE_MIN": cv2.REDUCE_MIN
}

RotateFlags = {
    "ROTATE_90_CLOCKWISE": cv2.ROTATE_90_CLOCKWISE,
    "ROTATE_180": cv2.ROTATE_180,
    "ROTATE_90_COUNTERCLOCKWISE": cv2.ROTATE_90_COUNTERCLOCKWISE
}
