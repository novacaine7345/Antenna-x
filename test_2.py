# test_vswr.py
from vswr_gpr_model import predict_vswr
from s11_gpr_model import predict_s11

mean_db, std_db = predict_vswr(10.0)
mean_s11, std_s11 = predict_s11(10.0)
print("VSWR at 10 GHz:", mean_db, "±", std_db)
print("S11 at 10Ghz:", mean_s11, "±", std_s11)
