function update(option) {
    $.get('get-popular-campaigns', { hours: option.value },
        (data) => {
            $('#campaigns-number').text('Number of Campaigns: ' + data['campaigns'].length);
            $("#campaigns").find("tr:gt(0)").remove();
            $.each(data['campaigns'], (i, campaign) => {
                $('<tr>').append(
                    $('<td>').text(campaign.name),
                    $('<td>').text(campaign.backers),
                    $('<td>').text(campaign.pledged)
                ).appendTo('#campaigns');
            })
        }
    );
}