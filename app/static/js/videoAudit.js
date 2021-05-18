function timecode(tt) {
  value = tt.innerHTML;
  let video = document.querySelector("#video");
  //00:00:06.79  minutes:seconds:Mseconds
  let regExTimeArr = value.split(":");
  let timeMin = regExTimeArr[0] * 60 * 1000;
  let timeSec = regExTimeArr[1] * 1000;
  let timeMs = timeMin + timeSec + regExTimeArr[2];
  video.currentTime = timeMs;
}
