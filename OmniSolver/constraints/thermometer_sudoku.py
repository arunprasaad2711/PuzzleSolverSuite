def ThermometerConstraints(self, thermometer_IDs):
    """
    Adds thermometer constraints to the model.

    Args:
        thermometer_IDs (list of lists): A list where each sublist represents a thermometer.
                                        Each sublist contains tuples (row, col) indicating the cells
                                        of the thermometer in order from bulb to tip.
    """
    
    for thermo_id, thermo_cells in enumerate(thermometer_IDs):
        # Extract the cells for this thermometer
        cells = [self.Cells[row][col] for row, col in thermo_cells]

        # Add increasing constraints along the thermometer
        for i in range(len(cells) - 1):
            self.Model.Add(cells[i] < cells[i + 1])

        print(f"Thermometer {thermo_id + 1} constraints added.")

def SlowThermometerConstraints(self, thermometer_IDs):
    """
    Adds slow thermometer constraints to the model.
    Digits along a slow-thermometer must increase or stay the same.

    Args:
        thermometer_IDs (list of lists): A list where each sublist represents a thermometer.
                                        Each sublist contains tuples (row, col) indicating the cells
                                        of the thermometer in order from bulb to tip.
    """
    
    for thermo_id, thermo_cells in enumerate(thermometer_IDs):
        # Extract the cells for this thermometer
        cells = [self.Cells[row][col] for row, col in thermo_cells]

        # Add increasing constraints along the thermometer
        for i in range(len(cells) - 1):
            self.Model.Add(cells[i] <= cells[i + 1])

        print(f"Slow Thermometer {thermo_id + 1} constraints added.")