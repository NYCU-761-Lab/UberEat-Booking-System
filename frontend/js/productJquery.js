// encode base64 image using javascript
let encodeImage = null;
// let hasImage = false;
function encodeImageFileAsURL(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        encodeImage = reader.result;
    }
    reader.readAsDataURL(file);
    // hasImage = true;
}

$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    let request_url = "http://127.0.0.1:8080";
    let globalStoreName = null;

    // every time we do some modify, refresh the list
    async function refreshProductList(shopName) {
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        let body = {
            'shop_name': shopName
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
                // console.log(myJson['Product list of the shop']);
                return myJson['Product list of the shop'];
            }
        });

        // clear html DOM first
        $(".shopProductResult").find('tbody').empty();
        for (i in productList) {
            let productName = productList[i][0];
            let productImg = productList[i][1];
            let productPrice = productList[i][2];
            let productQuantity = productList[i][3];

            // add elements to html DOM
            $(".shopProductResult").find('tbody')
            .append($('<tr>')
                .append($('<th>')
                    .attr('scope', 'row')
                    .text(Number(i) + 1)
                )
                .append($('<td>')
                    .append($('<img>')
                        .attr('src', productImg)
                        .attr('width', "180")
                        // .attr('height', "10")
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
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-info btn-edit')
                        .attr('id', 'editBtn_' + productName)
                        .attr('data-toggle', 'modal')
                        .attr('data-target', '#editModal')
                        .text('Edit')
                    )
                )
                .append($('<td>')
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-danger btn-delete')
                        .attr('id', 'deleteBtn_' + productName)
                        .text('Delete')
                    )
                )
            );
        }
    }

    $("#shopItem").click(async function() {
        let statusCode = null;
        let shopName = null;
        
        // Get shop's name
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        shopName = await fetch(request_url + "/shop/get_shop_name_of_user", {
            method: 'POST',
            headers: headers
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['shop_name of the user'];
            }
        });

        // 使用者沒有商店的情況會有後端擋掉，記得判斷
        if (shopName != null) {
            // show current products
            globalStoreName = shopName;
            refreshProductList(shopName);
        }
    });

    // add new product
    $(".addProductBtn").click(async function() {
        let shopName = null;
        let addMeal = $(".addMeal").val();
        let addPrice = $(".addPrice").val();
        let addQuantity = $(".addQuantity").val();
        let addImage = encodeImage;
        
        // Get shop's name
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        shopName = await fetch(request_url + "/shop/get_shop_name_of_user", {
            method: 'POST',
            headers: headers
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['shop_name of the user'];
            }
        });

        // add the product
        if (addMeal === "" || addPrice === "" || addQuantity === "" || addImage === null) {
            alert("The field cannot be left blank.");
        } else {
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'product_name': addMeal,
                'price': addPrice,
                'quantity': addQuantity,
                'picture': addImage
            }

            let statusCode = null;
            fetch(request_url + "/product/register", {
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
                    alert(myJson['message']);
                    refreshProductList(shopName);
                    $(".addMeal").val("");
                    $(".addPrice").val("");
                    $(".addQuantity").val("");
                    $(".addImage").val("");
                    encodeImage = null
                } else {
                    alert(myJson['message']);
                }
            });
        }
        // encodeImage = null;  // refresh
        // hasImage = false;  // refresh
    });


    // edit current product
    $(document).on('click', '.btn-edit', async function(e) {
        // get the store's information
        let targetProduct = e.target.id.slice(8);
        console.log(e.target.id);
        console.log(targetProduct);
        $(".edit-modal-text").text("edit " + targetProduct);

        $(".editBtn").unbind().click(async function() {
            let editPrice = $(".edit-price").val();
            let editQuantity = $(".edit-quantity").val();
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }

            if (editPrice === "" || editQuantity === "") {
                alert("The field cannot be left blank.");
            } else {
                // edit price
                let body = {
                    'product_name': targetProduct,
                    'edit_price': editPrice
                }
                await fetch(request_url + "/product/edit_price", { 
                    method: 'PUT',
                    headers: headers,
                    body: JSON.stringify(body)
                })
                .then(function(response) {
                    statusCode = response['status'];
                    return response.json();
                })
                .then(function(myJson) {
                    if (statusCode === 200) {
                        alert(myJson['message']);
                    } else {
                        alert(myJson['message']);
                    }
                });

                // edit quantity
                body = {
                    'product_name': targetProduct,
                    'edit_quantity': editQuantity
                }
                await fetch(request_url + "/product/edit_quantity", { 
                    method: 'PUT',
                    headers: headers,
                    body: JSON.stringify(body)
                })
                .then(function(response) {
                    statusCode = response['status'];
                    return response.json();
                })
                .then(function(myJson) {
                    if (statusCode === 200) {
                        alert(myJson['message']);
                    } else {
                        alert(myJson['message']);
                    }
                });
            }
            refreshProductList(globalStoreName);
        });
    });

    
    // delete current product
    $(document).on('click', '.btn-delete', async function(e) { 
        let statusCode = null;
        // Get shop's name
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let shopName = await fetch(request_url + "/shop/get_shop_name_of_user", {
            method: 'POST',
            headers: headers
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['shop_name of the user'];
            }
        });

        // delete the product
        let productDelete = e.target.id.slice(10);
        let body = {
            'product_name': productDelete
        }

        fetch(request_url + "/product/delete", {
            method: 'DELETE',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            console.log(response);
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            console.log(myJson);
            if (statusCode === 200) {
                alert(myJson['message']);
                refreshProductList(shopName);
            } else {
                alert(myJson['message']);
            }
        });
    });
});