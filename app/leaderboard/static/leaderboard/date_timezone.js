times = $(".schedule-time");

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

function format_date(date) {
  const month = MONTHS[date.getMonth()];
  const day = new String(date.getDate());
  const hour = new String(date.getHours()).padStart(2, "0");
  const minute = new String(date.getMinutes()).padStart(2, "0");
  return `${month} ${day}, ${hour}:${minute}`;
}

for (let i = 0; i < times.length; i++) {
  let span = times[i];
  let date = new Date(
    1000 * new Number(span.attributes["data-schedule-date"].value)
  );
  $(span).text(format_date(date));
}
