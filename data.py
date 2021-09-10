import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_filename = 'particles_temp.hdf5'
dataframe = pd.read_hdf(data_filename)
dataframe.index.name = 'index'

df = dataframe.set_index('particle')
particle_ids = np.unique(df.index.values)
print(particle_ids)

# Select a particle
particle_id = 9
particle_data = df.loc[particle_id]
# particle_data = particle_data.to_frame()
new_particle_data = particle_data.set_index('frame')
new_particle_data.head()

first_frame_of_particle = new_particle_data.index.min()
x_coord = new_particle_data['x'].loc[first_frame_of_particle]
y_coord = new_particle_data.loc[first_frame_of_particle]['y']

new_particle_data['rms'] = ((new_particle_data['x']-x_coord)**2 + (new_particle_data['y']-y_coord)**2)**0.5
print(new_particle_data.head())

#Plot using pandas
new_particle_data['rms'].plot()
#plot using matplotlib directly
frame_nums = new_particle_data['rms'].index.values
rms = new_particle_data['rms'].values
plt.plot(frame_nums, rms, 'r-')