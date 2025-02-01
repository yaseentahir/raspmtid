/**
 * Updates the current digit, distance and motor status calling
 * the corresponding methods.
 */
async function updateStatus() {
  // Update current digit based on Open CV

  //
  (async () => await updateCurrentDigitOpenCV())();

  //console.log("dfdg "+currentStatus.data)
  (async () => await updateMotorStatus())();
  // Update current distance
  (async () => await updateDistance())();
  // Update current digit based on OpenCV
  (async () => await updateCurrentDigitDistance())();
}

/**
 * Update the current digit based on OpenCV.
 */
async function updateCurrentDigitOpenCV() {
  try {
    // Request digit from server
    const requestResult = await requestDigitFromOpenCV();
    // Get the HTML element where the status is displayed
    console.log(requestResult.data);
    const eight_open_cv = document.getElementById("eight_open_cv");
    eight_open_cv.innerHTML = requestResult.data[0];
    const three_open_cv = document.getElementById("three_open_cv");
    three_open_cv.innerHTML = requestResult.data[1];
    const one_open_cv = document.getElementById("one_open_cv");
    one_open_cv.innerHTML = requestResult.data[2];
  } catch (e) {
    console.log("Error getting the digit based on OpenCV", e);
    updateStatus("Error getting the digit based on OpenCV");
  }
}

/**
 * Function to request the server to update the current
 * digit based on OpenCV.
 */
function requestDigitFromOpenCV() {
  try {
    // Make request to server
    return axios.get("/get_digit_from_opencv");
  } catch (e) {
    console.log("Error getting the status", e);
    updateStatus("Error getting the status");
  }
}

/**
 * Function to request the server to start the motor.
 */
function requestStartMotor() {
  try {
    // Make request to server
    return axios.get("/start_motor");
  } catch (e) {
    console.log("Error getting the status", e);
    updateStatus("Error getting the status");
  }
}

/**
 * Function to request the server to stop the motor.
 */
function requestStopMotor() {
  try {
    // Make request to server
    return axios.get("/stop_motor");
  } catch (e) {
    console.log("Error getting the status", e);
    updateStatus("Error getting the status");
  }
}

/**
 * Update the status of the motor.
 * @param {String} status
 */
async function updateMotorStatus() {
  // Get the HTML element where the status is displayed
  // ...
  const currentStatus = await request_motor_status();
  console.log("Status Calling");
  const motor_status = document.getElementById("motor_status");
  motor_status.innerHTML = currentStatus.data;
}
function request_motor_status() {
  try {
    // Make request to server
    return axios.get("/motor_status");
  } catch (e) {
    console.log("Error getting the status", e);
    updateStatus("Error getting the status");
  }
}
/**
 * Update the current digit based on distance sensor.
 */
async function updateTime() {
  // Get the HTML element where the status is displayed
  const currentStatus = await requestStopMotor();
  console.log("Status Calling");
  const motor_status = document.getElementById("moter_time");
  motor_status.innerHTML = currentStatus.data;
}
async function updateDistance() {
  // Get the HTML element where the status is displayed
  const currentStatus = await requestDistance();
  console.log("Status Calling");
  const motor_status = document.getElementById("distance");
  motor_status.innerHTML = currentStatus.data;
}
/**
 * Function to request the server to get the distance from
 * the rod to the ultrasonic sensor.
 */
function requestDistance() {
  try {
    // Make request to server
    return axios.get("/get_distance");
  } catch (e) {
    console.log("Error getting the status", e);
    updateStatus("Error getting the status");
  }
}

/**
 * Update the current digit based on distance sensor.
 */
async function updateCurrentDigitDistance() {
  try {
    // Request digit from server
    const requestResult = await requestDigitFromDistance();
    // Get the HTML element where the status is displayed
    const eight_distance = document.getElementById("eight_distance");
    eight_distance.innerHTML = requestResult.data[0];
    const three_distance = document.getElementById("three_distance");
    three_distance.innerHTML = requestResult.data[1];
    const one_distance = document.getElementById("one_distance");
    one_distance.innerHTML = requestResult.data[2];
  } catch (e) {
    console.log("Error getting the digit based on distance", e);
    updateStatus("Error getting the digit based on distance");
  }
}

/**
 * Function to request the server to get the digit based
 * on distance only.
 */
function requestDigitFromDistance() {
  try {
    // Make request to server
    return axios.get("/get_digit_from_distance");
  } catch (e) {
    console.log("Error getting the status", e);
    updateStatus("Error getting the status");
  }
}
