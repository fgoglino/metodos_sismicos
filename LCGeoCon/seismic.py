import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# DEFINE PARAMETERS
# =============================================================================

# SIMULATION PARAMETERS
thicks = [3, 17]
vels = [450, 1300, 1800]

sensors1 = np.floor(np.linspace(5,12,8))
sensors2 = (np.linspace(12 + 12, 12 + 16 * 12,16))
sensors = np.concatenate([sensors1, sensors2])

# SANITY CHECK THE PARAMETERS
if len(thicks) < 1:
    raise Exception("Vels must contain one more item than thicks")
if len(vels) != len(thicks) + 1:
    raise Exception("Thicks must not be an empty list") 

# =============================================================================
# FUNCTION DEFINITIONS
# =============================================================================

def direct(x, v):
    return (x / v)

def refract (x, interfaceIdx):
    ret = x / vels[interfaceIdx + 1]
    for aboveIdx in range(0, interfaceIdx + 1):
        theta = np.arcsin(vels[aboveIdx] / vels[interfaceIdx + 1])
        ret += 2 * thicks[aboveIdx] * np.cos(theta) / vels[aboveIdx]
        #print(ret)
    return ret

# CRITICAL REFRACTION DISTANCE FUNCTION
def xcrit(z, v1, v2):
    theta = np.arcsin(v1 / v2)
    return 2 * z * np.tan(theta)

# GENERAL TRAVEL TIME FUNCTION
def traveltimes(thicks, vels, sensors):
    
    # CALCULATE DIRECT TIME LIST
    tDrct = np.zeros(len(sensors))
    for sensIdx, sens in enumerate(sensors):
        tDrct[sensIdx] = direct(sens,vels[0])
    
    # CALCULATE REFRACTION TIME ARRAY (COL = SENSOR, ROW = LAYER)
    tRefr = np.zeros([len(thicks), len(sensors)])
    for sensIdx in range(0, len(sensors)):
        for layerIdx in range(0, len(thicks)):
            tRefr[layerIdx, sensIdx] = refract(sensors[sensIdx], layerIdx)
        
    return [tDrct, tRefr]

# =============================================================================
# MAIN FUNCTION BODY
# =============================================================================

[tDrct, tRefr] = traveltimes(thicks, vels, sensors)
print("1st refraction critical distance: " + str(xcrit(thicks[0], vels[0], vels[1])))
print("2nd refraction critical distance: " + str(xcrit(thicks[1], vels[1], vels[2])))

# PAST THIS POINT, JUST PLOTTING BOILERPLATE
fig, ax = plt.subplots(figsize=(6, 12))

ax1 = plt.subplot(2,1,1)
ax1.plot(sensors, tDrct, ".")
for i in range(0,len(thicks)):
    ax1.plot(sensors, tRefr[i,:], ".")
ax1.set_title('Caso X')
ax1.set_ylim([0, 0.2])
ax1.set_ylabel("Tiempo de arribo (s)")
ax1.set_xlabel("Distancia hotizontal (m)")
ax1.legend(["Directa", "1ra refracción", "2da refracción"])

ax2 = plt.subplot(2,1,2)
ax2.plot(sensors, tDrct, ".")
for i in range(0,len(thicks)):
    ax2.plot(sensors, tRefr[i,:], ".")
ax2.set_title('Caso X, primeros sensores')
ax2.set_ylim([0, 0.04])
ax2.set_xlim([4, 13])
ax2.set_ylabel("Tiempo de arribo (s)")
ax2.set_xlabel("Distancia a sensor (m)")
ax2.legend(["Directa", "1ra refracción", "2da refracción"])

plt.savefig('test.png', dpi=300)

