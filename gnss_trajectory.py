"""Generate position-trajectory CSV files for GNSS simulation.

Output format matches circle_llh.csv:
    time_seconds, latitude_degrees, longitude_degrees, altitude_meters

There is no header row. Defaults to one sample every 0.1 seconds.
"""

import math
from pathlib import Path


def _write_llh_csv(output_path, duration_s, sample_interval_s, position_at_time):
    """Write time/latitude/longitude/altitude samples to a headerless CSV."""
    if duration_s <= 0:
        raise ValueError("duration_s must be greater than zero")
    if sample_interval_s <= 0:
        raise ValueError("sample_interval_s must be greater than zero")

    # Use ceil so samples occur at t = 0, dt, 2*dt, ... while t < duration.
    sample_count = math.ceil(duration_s / sample_interval_s - 1e-12)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        for i in range(sample_count):
            t = i * sample_interval_s
            latitude, longitude, altitude = position_at_time(t)
            # Match the sample file's formatting and do not write a header.
            csv_file.write(
                f"{t:5.1f}, {latitude:.9f}, {longitude:.9f}, {altitude:10.3f}\n"
            )

    return output_path


def generate_stationary(
    output_path,
    latitude,
    longitude,
    duration_s,
    altitude_m=100.0,
    sample_interval_s=0.1,
):
    """Generate a stationary trajectory at one coordinate for duration_s."""
    if not -90 <= latitude <= 90:
        raise ValueError("latitude must be between -90 and 90 degrees")
    if not -180 <= longitude <= 180:
        raise ValueError("longitude must be between -180 and 180 degrees")

    def position_at_time(_t):
        return latitude, longitude, altitude_m

    return _write_llh_csv(
        output_path, duration_s, sample_interval_s, position_at_time
    )


def generate_straight_line(
    output_path,
    latitude,
    longitude,
    duration_s,
    axis,
    speed_mps,
    altitude_m=100.0,
    sample_interval_s=0.1,
):
    """Generate a straight north/south or east/west trajectory.

    Args:
        output_path: Destination CSV path.
        latitude, longitude: Starting coordinate in decimal degrees.
        duration_s: Duration in seconds; samples stop before this time.
        axis: "latitude" or "longitude".
        speed_mps: Signed speed in meters/second. For axis="latitude",
            positive increases latitude (north) and negative decreases it
            (south). For axis="longitude", positive increases longitude
            (east) and negative decreases it (west).
        altitude_m: Constant altitude in meters.
        sample_interval_s: Time between samples in seconds.

    This uses a local spherical-Earth approximation, suitable for simple
    simulated paths. Longitude motion is invalid at the exact poles.
    """
    if not -90 <= latitude <= 90:
        raise ValueError("latitude must be between -90 and 90 degrees")
    if not -180 <= longitude <= 180:
        raise ValueError("longitude must be between -180 and 180 degrees")
    if axis not in ("latitude", "longitude"):
        raise ValueError("axis must be 'latitude' or 'longitude'")
    if axis == "longitude" and abs(latitude) >= 90:
        raise ValueError("longitude movement is undefined at the exact poles")

    earth_radius_m = 6_371_000.0
    start_lat_rad = math.radians(latitude)

    def position_at_time(t):
        distance_m = speed_mps * t

        if axis == "latitude":
            new_latitude = latitude + math.degrees(distance_m / earth_radius_m)
            if not -90 <= new_latitude <= 90:
                raise ValueError(
                    "trajectory crosses a pole; reduce speed or duration"
                )
            return new_latitude, longitude, altitude_m

        # Distance per degree of longitude shrinks by cos(latitude).
        meters_per_degree_lon = (
            earth_radius_m * math.cos(start_lat_rad) * math.pi / 180.0
        )
        new_longitude = longitude + distance_m / meters_per_degree_lon
        # Wrap longitude into [-180, 180].
        new_longitude = (new_longitude + 180.0) % 360.0 - 180.0
        return latitude, new_longitude, altitude_m

    return _write_llh_csv(
        output_path, duration_s, sample_interval_s, position_at_time
    )



# Testing
generate_stationary(
    output_path="CoordinateFiles/stationary.csv",
    latitude=35.274015965,
    longitude=137.014864092,
    duration_s=300,
    altitude_m=100,
    sample_interval_s=0.1,
)

generate_straight_line(
    output_path="CoordinateFiles/moving_north.csv",
    latitude=35.274015965,
    longitude=137.014864092,
    duration_s=60,
    axis="latitude",
    speed_mps=100,
    altitude_m=100,
    sample_interval_s=0.1,
)
