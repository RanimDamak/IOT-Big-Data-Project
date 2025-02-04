setInterval(function() {
    // Make a request to the /kpi route to get the latest KPI values
    fetch('/kpi')
      .then(response => response.json())
      .then(kpi => {
        // Update the speed element
        document.getElementById('speed').innerHTML = kpi.speed;
        // Update the fuel consumption element
        document.getElementById('fuel-consumption').innerHTML = kpi.fuel_consumption;
        // Update the sudden acceleration element
        document.getElementById('sudden-acceleration').innerHTML = kpi.sudden_acceleration ? 'Yes' : 'No';
        // Update the sudden deceleration element
        document.getElementById('sudden-deceleration').innerHTML = kpi.sudden_deceleration ? 'Yes' : 'No';
        // Update the maximum speed element
        document.getElementById('max-speed').innerHTML = kpi.max_speed;
        // Update the minimum speed element
        document.getElementById('min-speed').innerHTML = kpi.min_speed;
        // Update the velocity standard deviation element
        document.getElementById('velocity-std').innerHTML = kpi.velocity_std;
        // Update the high RPM element
        document.getElementById('high-rpm').innerHTML = kpi.high_rpm ? 'Yes' : 'No';
        // Update the idling element
        document.getElementById('idling').innerHTML = kpi.idling ? 'Yes' : 'No';
        // Update the cruising element
        document.getElementById('cruising').innerHTML = kpi.cruising ? 'Yes' : 'No';
      });
  }, 1000); // Update the dashboard every second
  