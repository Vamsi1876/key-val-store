function success(data = {}){
    return {
        success: true,
        data,
        error : null
    }
}

function failure(error = "An error occurred"){
    return {
        success: false,
        data: null,
        error
    }
}

module.exports = {
    success,
    failure
}