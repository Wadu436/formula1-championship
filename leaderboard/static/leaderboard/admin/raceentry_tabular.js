"use strict";
{
  function updateOnChange() {
    let fields = $("tr:has(td.field-team):has(td.field-driver):visible");
    let api_base_url = $("#raceentry_set-group").attr("data-api-call");
    for (var i = 0; i < fields.length; i++) {
      let driver_select = $(fields[i]).find("td.field-driver > div > select");
      let team_select = $(fields[i]).find("td.field-team > div > select");
      if (driver_select.length !== 1 || team_select.length !== 1) {
        continue;
      }
      driver_select = driver_select[0];
      team_select = team_select[0];

      $(driver_select).unbind("change");

      $(driver_select).change((event) => {
        let driver_id = driver_select.value;
        if (driver_id) {
          $.get(
            api_base_url.replace("0", driver_id),
            null,
            (data) => {
              team_select.value = data.team || "";
            },
            "json"
          );
        } else {
          team_select.value = "";
        }
      });
    }
  }

  $(document).ready(function () {
    updateOnChange(); // To be 100% sure

    $("#raceentry_set-group tbody").bind("DOMSubtreeModified", function () {
      updateOnChange();
    });
  });
}
