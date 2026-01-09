## run code using:
```
gemini --mcp_allowed_server_names AFM_mcp Ferrosim_mcp
```

## give mcp the followin queries - 
What it can do:

   * Initialize and register data: It can set up a virtual STEM and load datasets from files.
   * Retrieve image data: It can provide a general overview image.
   * Access spectral data: It can extract full 3D spectrum images (a datacube with spatial and energy dimensions) or data from a single point within that image. It can also retrieve the energy axis 
     associated with a spectrum.

  Accepted Queries (Methods):
  #  ----- AFM --------
   * initialize_microscope(afm microscope):
    ```Sets up the microscope. ```
   * register_data(data_source)- H5 FILES:
     ```Loads a dataset from a file. ```
   * get_overview_image(): Returns a 2D overview image.
   * get_point_data(spectrum_image_index, x, y): Gets the spectrum data from a single (x, y) coordinate in a specified spectrum image.
   * get_spectrum_image(spectrum_image_index): Retrieves a full 3D spectrum image datacube.
   * get_spectrum_image_e_axis(spectrum_image_index): Returns the energy (E) axis for a given spectrum image.
  #  ----- FERROSIM-------
   * `run_ferro_simulation`: This tool takes your high-level parameters (n, alpha, beta, etc.), passes them to the Ferro2DSim class to run the entire process described above, and then returns a summary of 
     the results, including the total polarization over time and the maximum measured response.
   * `calculate_experiment_match`: This is a utility tool that allows you to compare the polarization history from your simulation with an experimental result by calculating the Root Mean Square Error 
     (RMSE), giving you a metric for how well your simulation parameters match the experiment.


