$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    const account = sessionStorage.getItem("accountStorage");
    let request_url = "http://127.0.0.1:8080";
    let shopSearchResult = [];  // 紀錄符合搜索條件的商店（1D array）
    let shopInfoResult = [];  // 紀錄符合搜索條件的商店的細節（要呈現在 HTML DOM 上的東西）(2D array)

    // get search result first
    async function getSearchResult () {
        shopInfoResult = [];
        for (i in shopSearchResult) {
            let storeName = shopSearchResult[i];
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
            shopInfoResult.push([storeName, storeType, storeDistance]);
        }
    }

    // show the result on the DOM after filter
    async function showSearchResult () {
        // clear html DOM first
        $(".searchResult").find('tbody').empty();

        // Show searching result
        for (i in shopSearchResult) {
            // get the information
            let storeName = shopInfoResult[i][0];
            let storeType = shopInfoResult[i][1];
            let storeDistance = shopInfoResult[i][2];
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
                        .attr('class', 'btn btn-info btn-open-menu')
                        .attr('id', 'openBtn_' + storeName)
                        .attr('data-toggle', 'modal')
                        .attr('data-target', '#all-modals')
                        .text('Open menu')
                    )
                )
            );
        }

        // show multiple pages
        $('#data').find('div').empty();
        $('#data').append($('<div>').attr('id', 'nav'));

        let rowsShown = 5;  // 每頁顯示幾個店家
        let rowsTotal = shopSearchResult.length;  
        let numPages = rowsTotal / rowsShown;
        for (i = 0; i < numPages; i++) {  
            let pageNum = i + 1;  
            $('#nav').append ('<a href="#" rel="' + i + '">' + pageNum + '</a>  ');  
        }  
        $('#data tbody tr').hide();  
        $('#data tbody tr').slice (0, rowsShown).show();  
        $('#nav a:first').addClass('active');  
        $('#nav a').bind('click', function() {  
            $('#nav a').removeClass('active');  
            $(this).addClass('active');  
                var currPage = $(this).attr('rel');  
                var startItem = currPage * rowsShown;  
                var endItem = startItem + rowsShown;  
                $('#data tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).  
                css('display','table-row').animate({opacity:1}, 300);  
        });  
    }

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

    // show the sorted result
    $('#shopSortBtn').click(function() {
        let sortType = $('#sortType').val();
        let sortMethod = $('#sortMethod').val();
        
        // sort shopSearchResult in ascending order
        if (sortType === "Shop Name") {
            shopInfoResult.sort(function(a, b) {
                let x = a[0].toLowerCase();
                let y = b[0].toLowerCase();
                if (x < y) { return -1; }
                if (x > y) { return 1; }
                return 0;
            });
        } else if (sortType === "Shop Category") {
            shopInfoResult.sort(function(a, b) {
                let x = a[1].toLowerCase();
                let y = b[1].toLowerCase();
                if (x < y) { return -1; }
                if (x > y) { return 1; }
                return 0;
            });
        } else if (sortType === "Shop Distance") {
            shopInfoResult.sort(function(a, b) { return a[2] - b[2] });
        }

        if (sortMethod === "Descend") shopInfoResult.reverse();
        showSearchResult();
    });


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
                    shopSearchResult = stores;
                    isFirstFilter = false;
                }
            });
        }

        // search distance
        let askShopDist = $("#sel1").val();
        let askShopDistNew = null;
        let headers_new = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }

        if (askShopDist[0] === "n") askShopDistNew = "near";
        if (askShopDist[0] === "m") askShopDistNew = "moderate";
        if (askShopDist[0] === "f") askShopDistNew = "far";

        body = {
            'req_distance': askShopDistNew
        }
        if (askShopDist != "no constraint") {
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
                    shopSearchResult = stores;
                    isFirstFilter = false;
                }
            });
        }

        // search price
        let askLowPrice = $(".askLowPricePlace").val();
        let askHighPrice = $(".askHighPricePlace").val();
        // cannot pass null to the body
        if (askLowPrice === "") askLowPrice = "null";
        if (askHighPrice === "") askHighPrice = "null";
        body = {
            'price_lower_bound': askLowPrice,
            'price_upper_bound': askHighPrice
        }
        await fetch(request_url + "/product/price_filer", {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            console.log(myJson);
            if (statusCode === 200) {
                stores = shopFilter(stores, myJson['valid_shops_name'], isFirstFilter);
                shopSearchResult = stores;
                isFirstFilter = false;
            } else {
                alert(myJson['message']);
            }
        });

        // search meal name
        let askMealName = $(".askMealPlace").val();
        body = {
            'ask_product_name': askMealName
        }
        if (askMealName != "") {
            await fetch(request_url + "/product/name_filter", {
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
                    shopSearchResult = stores;
                    isFirstFilter = false;
                }
            });
        }

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
                    shopSearchResult = stores;
                    isFirstFilter = false;
                }
            });
        }
        await getSearchResult();
        await showSearchResult();
    });


    // open the store menu
    $(document).on('click', '.btn-open-menu', async function(e) {
        // get the store's information
        let targetStore = e.target.id.slice(8);
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        let body = {
            'shop_name': targetStore
        }

        let productList = await fetch(request_url + "/product/list", { 
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
                return myJson['Product list of the shop'];
            }
        });

        // add products to html DOM
        $(".menuModals").find('tbody').empty();
        for (i in productList) {
            let productName = productList[i][0];
            let productImg = productList[i][1];
            let productPrice = productList[i][2];
            let productQuantity = productList[i][3];

            $(".menuModals").find('tbody')
            .append($('<tr>')
                .append($('<th>')
                    .attr('scope', 'row')
                    .text(Number(i) + 1)
                )
                .append($('<td>')
                    .append($('<img>')
                        .attr('src', productImg)
                        .attr('width', "100")
                        .attr('src', productImg)
                        .attr('alt', productName)
                    )
                )
                .append($('<td>')
                    .text(productName)
                )
                .append($('<td>')
                    .text(productPrice)
                )
                .append($('<td>')
                    .text(productQuantity)
                )
                .append($('<td>')
                    // .append($('<input type="checkbox">'))
                    // .attr('id', 'cbox' + i)
                    // .attr('value', productName)
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-light btn-minus')
                        .attr('id', 'minusBtn_' + productName)
                        .attr('style', 'margin-right: 5px;')
                        .text('-')
                    )
                    .append($('<span>')
                        .attr('id', 'orderCnt_' + productName)
                        .text(0)
                    )
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-light btn-add')
                        .attr('id', 'addBtn_' + productName)
                        .attr('style', 'margin-left: 5px;')
                        .text('+')
                    )
                )
            );

            $(".btn-calculatePrice").attr('id', 'btn-calculatePrice_' + targetStore);
        }
    });
});