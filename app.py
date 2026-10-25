# ==========================================
# CAI DAT THU VIEN
# ==========================================

!pip install numpy-financial pandas

import numpy_financial as npf
import numpy as np
import pandas as pd

# ==========================================
# 1. NHAP DU LIEU DU AN
# ==========================================

print("CHUONG TRINH DANH GIA DU AN DAU TU")

# Nhap so nam du an
n = int(input("Nhap so nam du an: "))

if n < 1:
    raise ValueError("So nam du an phai >= 1")

# Nhap von dau tu ban dau
initial_investment = -abs(float(
    input("Nhap von dau tu ban dau (nam 0): ")
))

# Nhap dong tien tung nam
cash_flows = []

for year in range(1, n + 1):
    cf = float(input(f"Nhap dong tien CF nam {year}: "))
    cash_flows.append(cf)

# Nhap cac lai suat
discount_rate = float(
    input("Nhap ty le chiet khau (%): ")
) / 100

finance_rate = float(
    input("Nhap lai suat tai tro MIRR (%): ")
) / 100

reinvest_rate = float(
    input("Nhap lai suat tai dau tu MIRR (%): ")
) / 100

if min(discount_rate, finance_rate, reinvest_rate) <= -1:
    raise ValueError("Cac lai suat phai lon hon -100%")

# ==========================================
# 2. TONG HOP DONG TIEN
# ==========================================

full_cash_flows = [initial_investment] + cash_flows

years = list(range(n + 1))

# ==========================================
# 3. TINH DONG TIEN CHIET KHAU
# ==========================================

discounted_cf = [
    cf / (1 + discount_rate) ** year
    for year, cf in zip(years, full_cash_flows)
]

# Dong tien luy ke
cumulative_cf = np.cumsum(full_cash_flows)

# Dong tien chiet khau luy ke
cumulative_pv = np.cumsum(discounted_cf)

# ==========================================
# 4. LAP BANG DONG TIEN
# ==========================================

df = pd.DataFrame({
    "Nam du an": years,
    "Dong tien CF": full_cash_flows,
    "PV(CF)": discounted_cf,
    "CF luy ke": cumulative_cf,
    "PV luy ke": cumulative_pv
})

print("\nBANG DONG TIEN DU AN")
print(df.to_string(index=False, float_format="%.2f"))

# ==========================================
# 5. TINH NPV
# ==========================================

npv = npf.npv(discount_rate, full_cash_flows)

# ==========================================
# 6. TINH IRR
# ==========================================

irr = npf.irr(full_cash_flows)

# ==========================================
# 7. TINH MIRR
# ==========================================

mirr = npf.mirr(
    full_cash_flows,
    finance_rate,
    reinvest_rate
)

# ==========================================
# 8. TINH BCR (PI)
# ==========================================

pv_inflows = sum(
    pv for pv in discounted_cf if pv > 0
)

pv_outflows = -sum(
    pv for pv in discounted_cf if pv < 0
)

if pv_outflows > 0:
    bcr = pv_inflows / pv_outflows
    pi = bcr
else:
    bcr = np.nan
    pi = np.nan

# ==========================================
# 9. TINH DPP
# ==========================================

dpp = None

if cumulative_pv[0] >= 0:
    dpp = 0.0
else:
    for i in range(1, len(cumulative_pv)):
        if cumulative_pv[i] >= 0:
            if discounted_cf[i] > 0:
                dpp = (
                    (i - 1)
                    + abs(cumulative_pv[i - 1])
                    / discounted_cf[i]
                )
            break

# ==========================================
# 10. HIEN THI KET QUA
# ==========================================

print("\n" + "=" * 45)
print("KET QUA DANH GIA DU AN")
print("=" * 45)

print(f"NPV  = {npv:,.2f}")

if np.isfinite(irr):
    print(f"IRR  = {irr * 100:.2f}%")
else:
    print("IRR  = Khong xac dinh")

if np.isfinite(mirr):
    print(f"MIRR = {mirr * 100:.2f}%")
else:
    print("MIRR = Khong xac dinh")

print(f"BCR  = {bcr:.4f}")
print(f"PI   = {pi:.4f}")

if dpp is not None:
    print(f"DPP  = {dpp:.2f} nam")
else:
    print("DPP  = Khong hoan von trong thoi gian du an")

# ==========================================
# 11. DANH GIA DU AN
# ==========================================

print("\nDANH GIA HIEU QUA DAU TU")

if npv > 0:
    print("NPV > 0: Du an co hieu qua theo NPV")
elif npv == 0:
    print("NPV = 0: Du an hoa von theo NPV")
else:
    print("NPV < 0: Du an khong dat yeu cau NPV")

if np.isfinite(irr):
    if irr > discount_rate:
        print("IRR > r: Du an dat yeu cau IRR")
    else:
        print("IRR <= r: Du an khong dat yeu cau IRR")

if np.isfinite(bcr):
    if bcr > 1:
        print("BCR > 1: Loi ich hien tai lon hon chi phi")
    else:
        print("BCR <= 1: Loi ich hien tai khong lon hon chi phi")

if dpp is not None:
    print("Du an hoan von chiet khau trong ky")
else:
    print("Du an chua hoan von chiet khau")

# Tinh FVCOF va FVCIF
FVCOF = sum(
    abs(cf) * (1 + discount_rate)**(n - t)
    for t, cf in enumerate(full_cash_flows)
    if cf < 0
)

FVCIF = sum(
    cf * (1 + discount_rate)**(n - t)
    for t, cf in enumerate(full_cash_flows)
    if cf > 0
)

# Tinh MIRR
mirr = (FVCIF / FVCOF)**(1/n) - 1

print(f"FVCOF = {FVCOF:.2f}")
print(f"FVCIF = {FVCIF:.2f}")
print(f"MIRR = {mirr * 100:.2f}%")
