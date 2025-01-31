from http import HTTPStatus


def test_axial_force(client):
    # Act
    response = client.post(
        '/effective_axial_force',
        json={
            'effective_lag_tension': 90000,
            'internal_pressure': 0,
            'cross_sectional_area': 0,
            'temperature_difference': 0,
            'temperature_coefficient': 0,
            'young_modulus': 0,
            'poisson_coefficent': 0,
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'effective_lag_tension': 90000.0,
        'internal_pressure': 0.0,
        'cross_sectional_area': 0.0,
        'temperature_difference': 0.0,
        'temperature_coefficient': 0.0,
        'young_modulus': 0.0,
        'poisson_coefficent': 0.0,
        'effective_axial_force': 90000.0,
    }
