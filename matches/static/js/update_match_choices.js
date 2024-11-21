document.addEventListener('DOMContentLoaded', function () {
    location_choices = document.getElementById('id_match_location').options;
    document.getElementById('id_home_team').addEventListener('change', function () {
        update_location_choices(location_choices);
    });
    document.getElementById('id_away_team').addEventListener('change', function () {
        update_location_choices(location_choices);
    });
    document.getElementById('magic_round').addEventListener('change', function () {
        update_location_choices(location_choices);
    });
});

function update_location_choices(location_choices) {
    home_team = document.getElementById('id_home_team').value;
    away_team = document.getElementById('id_away_team').value;
    console.log('Home team: ' + home_team);
    console.log('Away team: ' + away_team);

    updated_locations = [];

    for (var i = 0; i < location_choices.length; i++) {
        console.log('Checking: ' + location_choices[i].value);
        if (!(location_choices[i].value == home_team || //check home 
            location_choices[i].value == away_team || // check away
            location_choices[i].value == home_team + ' SND' || // check secondary home
            location_choices[i].value == away_team + ' SND' || // check secondary away
            location_choices[i].value == home_team + ' TRD' || // check tertiary home
            location_choices[i].value == away_team + ' THD' // check tertiary away

        )) {
            location_choices[i].style.display = 'none';
            console.log('Removing ' + location_choices[i].value);
        }
        else
        {
            location_choices[i].style.display = 'block';
            document.getElementById('id_match_location').value = location_choices[i].value;
        }
    };

    if (document.getElementById('magic_round').checked)
    {
        for (var i = 0; i < location_choices.length; i++)
        {
            if (location_choices[i].value.includes('BRI'))
            {
                location_choices[i].style.display = 'block';
                document.getElementById('id_match_location').value = location_choices[i].value;
            }
        }
    };
}