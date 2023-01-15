import clr

clr.AddReference(r"C:\Users\dgexi\OneDrive\Documents\Code\Java_script\val_overlay\ts\dist\Custom_dll\Gex_QR_Gen.dll")



Gex_QR = Program()

Gex_QR.QR_Code_gen("192.168.1.22","4444",r"C:\Users\dgexi\OneDrive\Documents\Code\Java_script\val_overlay\ts\dist\img\val_logo.jpg")