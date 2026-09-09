-- ============================================
-- TABLE 1: ECG DATA (AD8232 Sensor)
-- ============================================
-- Stores raw electrocardiogram readings from AD8232 sensor
-- One row inserted every 100ms when ECG data arrives

CREATE TABLE IF NOT EXISTS ecg_data (
    id SERIAL PRIMARY KEY,
    -- Unique ID for each row (auto-increments: 1, 2, 3...)

    timestamp TIMESTAMPTZ NOT NULL,
    -- When the ECG reading was taken (includes timezone)

    device_id VARCHAR(50) NOT NULL,
    -- Which device sent this data (e.g., "driver_001")

    ecg_voltage FLOAT NOT NULL
    -- Raw voltage from AD8232 ECG sensor (in volts)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_ecg_data_timestamp ON ecg_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_ecg_data_device_id ON ecg_data(device_id);


-- ============================================
-- TABLE 2: PPG DATA (MAX30102 Sensor)
-- ============================================
-- Stores raw photoplethysmography readings from MAX30102 sensor
-- One row inserted every 100ms when PPG data arrives

CREATE TABLE IF NOT EXISTS ppg_data (
    id SERIAL PRIMARY KEY,
    -- Unique ID for each row (auto-increments: 1, 2, 3...)

    timestamp TIMESTAMPTZ NOT NULL,
    -- When the PPG reading was taken (includes timezone)

    device_id VARCHAR(50) NOT NULL,
    -- Which device sent this data (e.g., "driver_001")

    ppg_ir INTEGER NOT NULL,
    -- Infrared light intensity from MAX30102 (0-65535)

    ppg_red INTEGER NOT NULL
    -- Red light intensity from MAX30102 (0-65535)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_ppg_data_timestamp ON ppg_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_ppg_data_device_id ON ppg_data(device_id);


-- ============================================
-- TABLE 3: MPU6050 DATA (Motion Sensor)
-- ============================================
-- Stores raw acceleration/motion readings from MPU6050 sensor
-- One row inserted every 100ms when motion data arrives

CREATE TABLE IF NOT EXISTS mpu6050_data (
    id SERIAL PRIMARY KEY,
    -- Unique ID for each row (auto-increments: 1, 2, 3...)

    timestamp TIMESTAMPTZ NOT NULL,
    -- When the motion reading was taken (includes timezone)

    device_id VARCHAR(50) NOT NULL,
    -- Which device sent this data (e.g., "driver_001")

    acceleration_x FLOAT NOT NULL,
    -- X-axis acceleration from MPU6050 (in g, where g = 9.8 m/s²)

    acceleration_y FLOAT NOT NULL,
    -- Y-axis acceleration from MPU6050 (in g)

    acceleration_z FLOAT NOT NULL
    -- Z-axis acceleration from MPU6050 (in g)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_mpu6050_data_timestamp ON mpu6050_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_mpu6050_data_device_id ON mpu6050_data(device_id);


-- ============================================
-- TABLE 4: TEMPERATURE DATA (GY-906 Sensor)
-- ============================================
-- Stores raw temperature readings from GY-906 non-contact sensor
-- One row inserted every 100ms when temperature data arrives

CREATE TABLE IF NOT EXISTS temperature_data (
    id SERIAL PRIMARY KEY,
    -- Unique ID for each row (auto-increments: 1, 2, 3...)

    timestamp TIMESTAMPTZ NOT NULL,
    -- When the temperature reading was taken (includes timezone)

    device_id VARCHAR(50) NOT NULL,
    -- Which device sent this data (e.g., "driver_001")

    temperature_c FLOAT NOT NULL
    -- Temperature from GY-906 non-contact sensor (in Celsius)
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_temperature_data_timestamp ON temperature_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_temperature_data_device_id ON temperature_data(device_id);
