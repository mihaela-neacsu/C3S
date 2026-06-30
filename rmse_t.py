import xarray as xr
import numpy as np

ds1 = xr.open_dataset("forec.nc")
ds2 = xr.open_dataset("obs.nc", drop_variables=["days_bnds"])
var1 = ds1["var167"]
var2 = ds2["tavg"]
print(var1)
print(var2)
var2_fixed = (
       var2
       .rename({"days": "time"})
       .assign_coords(
           Latitude=var1.Latitude,
           Longitude=var1.Longitude
       )
       .broadcast_like(var1)
)

error = var1 - var2_fixed
error.to_netcdf("error.nc")

rmse_total = ((error ** 2).mean()) ** 0.5
rmse_total.to_netcdf("rmse_total.nc")

rmse_time = ((error ** 2).mean(dim=["lat", "lon"])) ** 0.5
rmse_time.to_netcdf("rmse_time.nc")

rmse_map = ((error ** 2).mean(dim="time")) ** 0.5
rmse_map.to_netcdf("rmse_map.nc")

rmse_idx = rmse_time.assign_coords(
        idx=("time", np.arange(rmse_time.sizes["time"]))
        )
rmse_sorted = rmse_idx.sortby(rmse_idx)
rmse_sorted.to_netcdf("rmse_time_sorted.nc")
print(rmse_sorted.isel(time=slice(0, 15)))

rmse_sorted = rmse_sorted.swap_dims({"time": "idx"})
rmse_sorted = rmse_sorted.drop_vars("time")
rmse_sorted.to_netcdf("rmse_memb_sorted.nc")

