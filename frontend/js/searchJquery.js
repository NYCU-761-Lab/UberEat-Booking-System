$(document).ready(function() {
    const accessToken = localStorage.getItem("tokenStorage");
    const account = localStorage.getItem("accountStorage");
    let request_url = "http://127.0.0.1:8080";

    // Filter the shop
    // stores: current record valid store
    // validStores: new record valid store
    function shopFilter (stores, validStores, isFirstFilter) {
        newStores = []
        if (isFirstFilter) {
            // push all unique items into newStores
            for (i in validStores) {
                if (newStores.includes(validStores[i]) === false) {
                    newStores.push(validStores[i]);
                }
            }
        } else {
            // remove the store if it is in stores but not in valid store
            for (i in stores) {
                if (validStores.includes(stores[i]) === true) {
                    newStores.push(stores[i]);
                }
            }
        }
        return newStores;
    }

    // search for shop
    $('#shopSearchBtn').click(async function() {
        let isFirstFilter = true;  // record which one is the first filter
        let stores = []  // record filter result
        let statusCode = null;

        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        // search shop name
        let askShopName = $('.askShopPlace').val();
        let body = {
            'ask_shop_name': askShopName
        }
        if (askShopName != "") {
            await fetch(request_url + "/shop/name_filter", {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    stores = shopFilter(stores, myJson['valid_shops_name'], isFirstFilter);
                    isFirstFilter = false;
                }
            });
        }

        // search distance
        let askShopDist = $("#sel1").val();
        let headers_new = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        body = {
            'req_distance': askShopDist
        }
        if (askShopDist != "") {
            await fetch(request_url + "/shop/distance_filter", {
                method: 'POST',
                headers: headers_new,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    stores = shopFilter(stores, myJson['valid_shops_name'], isFirstFilter);
                    isFirstFilter = false;
                }
            });
        }
        // search price


        // search meal

        // search category
        let askShopType = $(".askTypePlace").val();
        body = {
            'req_type': askShopType
        }
        if (askShopType != "") {
            await fetch(request_url + "/shop/type_filter", {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    stores = shopFilter(stores, myJson['valid_shops_name'], isFirstFilter);
                    isFirstFilter = false;
                }
            });
        }
        
        // clear html DOM first
        $(".searchResult").find('tbody').empty();

        // Show searching result
        console.log(stores);
        for (i in stores) {
            // get the information
            let storeName = stores[i];
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'shop_name': storeName,
            }

            let storeType = await fetch(request_url + "/shop/get_shop_type", { 
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    return myJson['shop_type of the shop_name'];
                }
            });

            let storeDistance = await fetch(request_url + "/shop/get_shop_distance", { 
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                if (statusCode === 200) {
                    return myJson['Distance to the shop (km)'];
                }
            });

            let targetString = '#' + storeName;
            // add elements to html DOM
            $(".searchResult").find('tbody')
            .append($('<tr>')
                .append($('<th>')
                    .attr('scope', 'row')
                    .text(Number(i) + 1)
                )
                .append($('<td>')
                    .text(storeName)
                )
                .append($('<td>')
                    .text(storeType)
                )
                .append($('<td>')
                    .text(storeDistance)
                )
                .append($('<td>')
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-info')
                        .attr('data-toggle', 'modal')
                        .attr('data-target', targetString)
                        .text('Open menu')
                    )
                )
            );
        }

    });
});