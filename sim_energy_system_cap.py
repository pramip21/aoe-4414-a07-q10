# sim_energy_system_cap.py
# Usage: python3 script_name.py arg1 arg2 ...
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by Pramil Patel
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math
import csv

# "constants"
# e.g., R_E_KM = 6378.137
# helper functions

## function description
# def calc_something(param1, param2):
#   pass

# initialize script arguments
# arg1 = '' # description of argument 1
# arg2 = '' # description of argument 2

# parse script arguments
# if len(sys.argv)==3:
#   arg1 = sys.argv[1]
#   arg2 = sys.argv[2]
#   ...
# else:
#   print(\
#    'Usage: '\
#    'python3 arg1 arg2 ...'\
#   )
#   exit()

# write script below this line

if len(sys.argv)==11:
  sa_m2 = float(sys.argv[1])
  eff = float(sys.argv[2])
  voc = float(sys.argv[3])
  c_f = float(sys.argv[4])
  r_esr = float(sys.argv[5])
  q0_c = float(sys.argv[6])
  p_on_w = float(sys.argv[7])
  v_thresh = float(sys.argv[8])
  dt_s = float(sys.argv[9])
  dur_s = float(sys.argv[10])
else:
  print("Usage: python3 sim_energy_system_cap.py sa_m2 eff voc c_f r_esr q0_c p_on_w v_thresh dt_s dur_s")


irr_w_m2 = 1366.1
log=[]

def calc_solar_current(irr_w_m2, sa_m2, eff, voc):
    return irr_w_m2*sa_m2*eff/voc

def calc_node_discr(q_c, c_f, i_a, esr_ohm, power_w):
    return (q_c/c_f + i_a*esr_ohm)**2 - 4*power_w*esr_ohm

def calc_node_voltage(disc, q_c, c_f, i_a, esr_ohm):
    return 0.5*(q_c/c_f + i_a*esr_ohm + math.sqrt(disc))

isc_a = calc_solar_current(irr_w_m2, sa_m2, eff, voc)
i1_a = isc_a
qt_c = q0_c
p_mode_w = p_on_w
t_s = 0.0
node_discr = calc_node_discr(qt_c, c_f, i1_a, r_esr, p_mode_w)
if(node_discr<0.0):
   p_mode_w = 0.0
   node_discr = calc_node_discr(qt_c, c_f, i1_a, r_esr, p_mode_w)

node_v = calc_node_voltage(node_discr, qt_c, c_f, i1_a, r_esr)
if voc<=node_v and i1_a!=0.0:
   i1_a = 0.0

if node_v<v_thresh:
   p_mode_w = p_on_w

log.append([t_s,node_v])

while t_s<dur_s:
    t_s += dt_s
    if node_v>0:
        i3_a = p_mode_w/node_v
    else:
       i3_a=0
    qt_c += (i1_a-i3_a)*dt_s
    if qt_c<0.0:
       qt_c = 0.0

    if 0<=node_v<voc:
       i1_a=isc_a
    else:
       i1_a=0.0   
   
    if p_mode_w==0.0 and node_v>=voc:
       p_mode_w = p_on_w

    node_discr = calc_node_discr(qt_c, c_f, i1_a, r_esr, p_mode_w)
    if (node_discr<0.0):
       p_mode_w = 0.0
       node_discr = calc_node_discr(qt_c, c_f, i1_a, r_esr, p_mode_w)
    node_v = calc_node_voltage(node_discr, qt_c, c_f, i1_a, r_esr)
    if voc<=node_v and i1_a!=-0.0:
       i1_a = 0.0
    if node_v<v_thresh:
       p_mode_w = 0.0
    log.append([t_s,node_v])
    
with open('./log.csv',mode='w',newline='') as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(['t_s','volts'])
    for e in log:
        csvwriter.writerow(e)
