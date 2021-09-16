import pyoo
import os
import string
import matplotlib.pyplot as plt
import math
import numpy as np

def c2n(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def init_pyoo():
    os.system('soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault # --headless')
    desktop = pyoo.Desktop('localhost', 2002)
    return desktop

def get_data(sheet, x0,x1,y0,y1):
    return sheet[y0-1:y1,c2n(x0)-1:c2n(x1)]
    
def get_data2(sheet,p0,p1):
	x0 = ""
	y0 = ""
	x1 = ""
	y1 = ""
	for c in p0:
		if c.isalpha():
			x0 = x0 + c
		else:
			y0 = y0 + c
	for c in p1:
		if c.isalpha():
			x1 = x1 + c
		else:
			y1 = y1 + c

	return sheet[int(y0)-1:int(y1),c2n(x0)-1:c2n(x1)]

def extract_data(cells):
    
    nrows = len(cells)
    ncols = len(cells[0])

    header = []
    
    for ii in range(0,ncols):
        header.append(cells[0][ii].value)
    
    data = []
    for ii in range(0,ncols):
        col = []
        for jj in range(1,nrows):
            val = cells[jj][ii].value
            
            if not isinstance(val,str): 
                val = int(val) if val % 1 == 0 else val
            
            if val != "---":
                col.append(val)
            else:
                col.append(float('nan'))
        data.append(col)

    return header, data

def extract_data(cells):

    nrows = len(cells)
    ncols = len(cells[0])

    header = []

    for ii in range(0,ncols):
        header.append(cells[0][ii].value)

    data = []
    for ii in range(0,ncols):
        col = []
        for jj in range(1,nrows):
            val = cells[jj][ii].value

            if not isinstance(val,str):
                val = int(val) if val % 1 == 0 else val

            if val != "---":
                col.append(val)
            else:
                col.append(float('nan'))
        data.append(col)

    return header, data

def extract_data_noheader(cells):

    nrows = len(cells)
    ncols = len(cells[0])

    data = []
    for ii in range(0,ncols):
        col = []
        for jj in range(0,nrows):
            val = cells[jj][ii].value

            if not isinstance(val,str):
                val = int(val) if val % 1 == 0 else val

            if val != "---":
                col.append(val)
            else:
                col.append(float('nan'))
        data.append(col)

    return data

def plot_classic(header, data):

    xname = header[0]
    ynames = header[1:]

    x = data[0]
    yarray = data[1:]
    
    fig, ax = plt.subplots()
    linestyle = [
        'solid', 'dotted', 'dashed', 'dashdot', (0, (1, 5)),
        (0, (3, 1, 1, 1)), (0, (3, 5, 1, 5))] 

    for ii in range(0,len(ynames)):
        ax.plot(x,yarray[ii],linestyle=linestyle[ii],label = ynames[ii])

    return fig, ax

def add_names(fig, xlabel, ylabel, xunits = None, yunits = None):
    xstr = xlabel
    ystr = ylabel
    if xunits:
        xstr = xstr + " [" + xunits + "]"
    if yunits:
        ystr = ystr + " [" + yunits + "]"
    fig.set_xlabel(xstr)
    fig.set_ylabel(ystr)


def latex_table(header, data, precision):
    
    nrows = len(max(data, key=len))
    ncols = len(header)

    # table options
    table = "\\begin{tabular}{" + ncols * "r" + "}\n \\hline\n"
    
    # column names
    table = table + " & ".join([cell for cell in header]) + "\\\\ \\hline \n" 

    rowdata = []

    #column values
    for irow in range(0,nrows):
        for icol in range(0,ncols):
            delim = ""
            if icol != ncols-1:
                delim = " & "
            val = data[icol][irow]
            valstr = ""
            if not isinstance(val, str) and math.isnan(val):
                valstr = "---"
            elif isinstance(val,str):
                valstr = val
            else:
                if isinstance(val, int):
                    valstr = str(val)
                else:
                    valstr = '%.*f' % (precision, val)
            table = table + valstr + delim
        table = table + " \\\\ \n"

    table = table + "\\hline \n" + "\\end{tabular}"

    return table
    
def save_table(fname, string):
    f = open(fname, "w")
    f.write(string)
    f.close()

desktop = init_pyoo()
doc = desktop.open_spreadsheet("../../precision.ods")
plt.style.use('science')
plt.rcParams.update({
    "font.size":10})          # specify font size here 
    
    
# =========================================================
# ================= DENSITY MATRIX/CHOLESKY ===============
# =========================================================

arrayDO = np.loadtxt('densityO.dat')
arrayLO = np.loadtxt('choleskyO.dat')
arrayDV = np.loadtxt('densityV.dat')
arrayLV = np.loadtxt('choleskyV.dat')

fig, ax = plt.subplots()
im = ax.imshow(arrayDO)
fig.savefig("densityO.pdf")

fig, ax = plt.subplots()
im = ax.imshow(arrayLO)
fig.savefig("choleskyO.pdf")

fig, ax = plt.subplots()
im = ax.imshow(arrayDV)
fig.savefig("densityV.pdf")

fig, ax = plt.subplots()
im = ax.imshow(arrayLV)
fig.savefig("choleskyV.pdf")

#exit(0)

# =========================================================
# ========== SPARSITY DEMONSTRATION =======================
# =========================================================

# ========= OVERLAP DECAY ==============

sheet = doc.sheets[7]

cells = get_data2(sheet, 'A3', 'D20')
data = extract_data_noheader(cells)

x = data[0]
y = data[1]

fig, ax = plt.subplots()

ax.plot(x,y,label="S$_{\\mu\\nu}$")
ax.legend()
ax.set_xlabel("r$_{\\mu\\nu}$ [a$_{0}$]")

fig.savefig("overlap_decay.pdf")

# ======== ELECTRON REPULSION DECAY ======

fig, ax = plt.subplots()
ax.plot(x,data[2],linestyle='solid',label="$(\\mu\\nu\\mid\\mu\\nu)$")
ax.plot(x,data[3],linestyle='dotted',label="$(\\mu\\mu\\mid\\nu\\nu)$")
ax.legend()
ax.set_xlabel("r$_{\\mu\\nu}$ [a$_{0}$]")

fig.savefig("eri_decay.pdf")

# ======= OVERLAP SPARSITY ===========

cells = get_data2(sheet, 'F2', 'I20')
data2 = extract_data_noheader(cells)
x = [i for i in range(1,len(data2[0])+1)]
y1 = data2[0]
y2 = data2[2]

fig, ax = plt.subplots()
ax.plot(x,y2,linestyle='solid',label="dense (N$^2$)")
ax.plot(x,y1,linestyle='dotted',label="sparse")
ax.legend()
ax.set_xlabel("Number of H atoms")
ax.set_ylabel("Number of elements")

fig.savefig("overlap_nze.pdf")

# ====== ERI SPARSITY =======

y3=data2[1]
y4=data2[3]

fig, ax = plt.subplots()
ax.plot(x,y4,linestyle='solid',label="dense (N$^4$)")
ax.plot(x,y3,linestyle='dotted',label="sparse")
ax.legend()
ax.set_xlabel("Number of H atoms")
ax.set_ylabel("Number of elements")

fig.savefig("eri_nze.pdf")

# ====== DENSITY SPARSITY =========

cells = get_data2(sheet, 'A45', 'E65')
header, data = extract_data(cells)

fig, ax = plt.subplots()

ax.plot(data[0],data[3],linestyle='solid',label="H chain")
ax.plot(data[0],data[4],linestyle='dotted',label="He chain")

add_names(ax, "r$_{\\mu \\nu}$ [a$_{0}$]", "$log|P_{\\mu\\nu}|$", None, None)
ax.legend(loc="best")
ax.set_yscale("log")

fig.savefig("density_decay.pdf")

#plt.show()

# =======================================================
# ================ SPARSITY 3C2E ========================
# =======================================================

cells = get_data2(sheet, 'A24', 'F43')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "r$_{\\mu P}$ [a$_{0}$]", "$|B_{\\mu\\mu}^{P}|$", None, None)
ax.legend(loc="best")

fig.savefig("ldf.pdf")


doc.close()
exit(0)

# =========== HARTREE FOCK ALKAN ==========================

cells = get_data2(sheet, 'A19', 'D23')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("hfK1_alkan.pdf")

# PLOT

cells = get_data2(sheet, 'A26', 'E30')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("hfK2_alkan.pdf")

# PLOT

cells = get_data2(sheet, 'A33', 'D37')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("hfJ_alkan.pdf")

# PLOT

cells = get_data2(sheet, 'A40', 'D44')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Non-Zero Elements", None, None)
ax.legend(loc="best")

fig.savefig("eri_nze_alkan.pdf")

# PLOT

cells = get_data2(sheet, 'A47', 'D51')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Non-Zero Elements", None, None)
ax.legend(loc="best")

fig.savefig("cfit_nze_alkan.pdf")

# ============== HARTREE FOCK FW ============================

cells = get_data2(sheet, 'G19', 'J23')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("hfK1_fw.pdf")

# PLOT

cells = get_data2(sheet, 'G26', 'I30')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("hfK2_fw.pdf")

# PLOT

cells = get_data2(sheet, 'G33', 'J37')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("hfJ_fw.pdf")

# PLOT

cells = get_data2(sheet, 'G40', 'J44')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Non-Zero Elements", None, None)
ax.legend(loc="best")

fig.savefig("eri_nze_fw.pdf")

# PLOT

cells = get_data2(sheet, 'G47', 'J51')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Non-Zero Elements", None, None)
ax.legend(loc="best")

fig.savefig("cfit_nze_fw.pdf")

# ====================== MP2 ALKAN ===============================

# PLOT

cells = get_data2(sheet, 'A65', 'D69')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("mp2_alkan.pdf")

# PLOT

cells = get_data2(sheet, 'A72', 'D76')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Non-Zero Elements", None, None)
ax.legend(loc="best")

fig.savefig("ftmp2_nze_alkan.pdf")

# ====================== MP2 FW ===============================

# PLOT

cells = get_data2(sheet, 'G65', 'J69')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Time", None, "s")
ax.legend(loc="best")

fig.savefig("mp2_fw.pdf")

# PLOT

cells = get_data2(sheet, 'G72', 'J76')
header, data = extract_data(cells)

fig, ax = plot_classic(header, data)
add_names(ax, "Number of basis functions", "Non-Zero Elements", None, None)
ax.legend(loc="best")

fig.savefig("ftmp2_nze_fw.pdf")

# ================== TABLES HARTREE FOCK ============================

# TABLE 

cells = get_data2(sheet, 'M19', 'W24')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("hf_scale_alkan.tex", table)

# TABLE

cells = get_data2(sheet, 'M28', 'W33')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("hf_scale_fw.tex", table)

# ================ TABLES MOLLER PLESSET ===================

# TABLE

cells = get_data2(sheet, 'M52', 'P56')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("mp_scale_alkan.tex", table)

# TABLE

cells = get_data2(sheet, 'M59', 'P63')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("mp_scale_fw.tex", table)

# TABLE

cells = get_data2(sheet, 'A79', 'C83')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("mp_cholesky.tex", table)

# ============== ACCURACIES ===================

# TABLE

cells = get_data2(sheet, 'Y25', 'AB31')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("hf_accuracy.tex", table)

# TABLE

cells = get_data2(sheet, 'Y42', 'AB48')
header, data = extract_data(cells)

table = latex_table(header, data, 2)
save_table("mp_accuracy.tex", table)

# fig.savefig("erissparsealkan.pdf")

# # DFIT SPARSITY

# cells = get_data(sheet, 'H', 'K', 24, 28)
# header, data = extract_data(cells)

# fig, ax = plot_classic(header, data)
# add_names(ax, "Number of basis functions", "Block Sparsity", None, "%")
# ax.legend(loc="best")
# ax.set_yscale("log")

# fig.savefig("dfsparsealkan.pdf")

# # ERIS nele

# cells = get_data(sheet, 'H', 'K', 31, 35)
# header, data = extract_data(cells)

# for icol in range(1,len(data)):
	# for irow in range(0,len(data[icol])):
		# val = 8 * data[icol][irow] / 1e+9
		# data[icol][irow] = val 
		
# fig, ax = plot_classic(header, data)

# add_names(ax, "Number of basis functions", "Memory", None, "GB")
# ax.legend(loc="best")
# ax.set_yscale("log")

# fig.savefig("erismemory.pdf")

# # dfit nele

# cells = get_data(sheet, 'H', 'K', 38, 42)
# header, data = extract_data(cells)

# for icol in range(1,len(data)):
	# for irow in range(0,len(data[icol])):
		# val = 8 * data[icol][irow] / 1e+9
		# data[icol][irow] = val 
		
# fig, ax = plot_classic(header, data)

# add_names(ax, "Number of basis functions", "Memory", None, "GB")
# ax.legend(loc="best")
# ax.set_yscale("log")

# fig.savefig("dfmemory.pdf")

# # PLOT MPALKANE

# cells = get_data(sheet, 'B', 'E', 32, 36)
# header, data = extract_data(cells)

# fig, ax = plot_classic(header, data)
# add_names(ax, "Number of basis functions", "Time", None, "s")
# ax.legend(loc="best")

# fig.savefig("mpmetric.pdf")

# # PLOT ADCALKANE

# cells = get_data(sheet, 'B', 'D', 51, 55)
# header, data = extract_data(cells)

# fig, ax = plot_classic(header, data)
# add_names(ax, "Number of basis functions", "Time", None, "s")
# ax.legend(loc="best")

# fig.savefig("adcmetric.pdf")

# # PLOT ADCSIGMA

# cells = get_data(sheet, 'B', 'G', 65, 69)
# header, data = extract_data(cells)

# fig, ax = plot_classic(header, data)
# add_names(ax, "Number of basis functions", "Time", None, "s")
# ax.legend(loc="best")

# fig.savefig("adcsigma.pdf")

# # ADC SPARSITY

# cells = get_data(sheet, 'B', 'F', 72, 76)
# header, data = extract_data(cells)

# fig, ax = plot_classic(header, data)
# add_names(ax, "Number of basis functions", "Block Sparsity", None, None)
# ax.legend(loc="best")
# ax.set_yscale("log")

# fig.savefig("adcsparse.pdf")

# # TABLE: hfexchange_scale

# cells = get_data(sheet, 'M', 'Q', 3, 7)
# header, data = extract_data(cells)

# table = latex_table(header, data, 2)
# save_table("hfexchange_scale.tex", table)

# # TABLE: dfit_scale

# cells = get_data(sheet, 'M', 'P', 17, 21)
# header, data = extract_data(cells)

# table = latex_table(header, data, 2)
# save_table("dfit_scale.tex", table)

# # TABLE: hfexchangefw_scale

# cells = get_data(sheet, 'M', 'P', 9, 13)
# header, data = extract_data(cells)

# table = latex_table(header, data, 2)
# save_table("hfexchangefw_scale.tex", table)

# # TABLE: dfitfw_scale

# cells = get_data(sheet, 'M', 'P', 25, 29)
# header, data = extract_data(cells)

# table = latex_table(header, data, 2)
# save_table("dfitfw_scale.tex", table)

# # TABLE hfprec

# cells = get_data(sheet, 'M', 'P', 55, 61)
# header, data = extract_data(cells)

# for icol in range(1,len(data)):
	# for irow in range(0,len(data[icol])):
		# data[icol][irow] = data[icol][irow] / 1e-6
		
# print(data)

# table = latex_table(header, data, 1)
# save_table("hfprec.tex", table)

# # TABLE: mp_scale

# cells = get_data(sheet, 'M', 'P', 32, 36)
# header, data = extract_data(cells)

# table = latex_table(header, data, 2)
# save_table("mp_scale.tex", table)

# # TABLE mpprec

# cells = get_data(sheet, 'M', 'P', 72, 78)
# header, data = extract_data(cells)

# for icol in range(1,len(data)):
	# for irow in range(0,len(data[icol])):
		# data[icol][irow] = data[icol][irow] / 1e-6
		
# print(data)

# table = latex_table(header, data, 1)
# save_table("mpprec.tex", table)

# # TABLE: adc_scale

# cells = get_data(sheet, 'B', 'D', 58, 62)
# header, data = extract_data(cells)

# table = latex_table(header, data, 2)
# save_table("adc_scale.tex", table)

#plt.show()

doc.close()

