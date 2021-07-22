import h5py

f = h5py.File('2021-07-21 11:59:22.hdf5', 'r')
print(list(f.keys()))
dset = f['ev_data']
print(dset[()])
f.close()
