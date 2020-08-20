data "azurerm_storage_account_sas" "sas" {
    connection_string = "${azurerm_storage_account.storage.primary_connection_string}"
    https_only = true
    start = "${formatdate("YYYY-MM-DD", timestamp())}"
    expiry = "${formatdate("YYYY-MM-DD", timeadd(timestamp(), "8760h"))}"
    resource_types {
        object = true
        container = false
        service = false
    }
    services {
        blob = true
        queue = false
        table = false
        file = false
    }
    permissions {
        read = true
        write = false
        delete = false
        list = false
        add = false
        create = false
        update = false
        process = false
    }
}

resource "azurerm_app_service_plan" "asp" {
    name = "${var.prefix}-plan"
    resource_group_name = "${azurerm_resource_group.rg.name}"
    location = "${var.location}"
    kind = "FunctionApp"
    sku {
        tier = "Dynamic"
        size = "Y1"
    }
}

resource "azurerm_function_app" "functions" {
    name                        = "${var.prefix}-${var.environment}"
    location                    = var.location
    resource_group_name         = azurerm_resource_group.rg.name
    app_service_plan_id         = azurerm_app_service_plan.asp.id
    storage_connection_string   = azurerm_storage_account.storage.primary_connection_string
    version                     = "~3"
    os_type                     = "linux"

    app_settings                = {
                        https_only = true
                        FUNCTIONS_WORKER_RUNTIME = "python"
                        FUNCTION_APP_EDIT_MODE = "readonly"
                        HASH = "${base64encode(filesha256("${var.functionapp}"))}"
                        WEBSITE_RUN_FROM_PACKAGE = "https://${azurerm_storage_account.storage.name}.blob.core.windows.net/${azurerm_storage_container.deployments.name}/${azurerm_storage_blob.appcode.name}${data.azurerm_storage_account_sas.sas.sas}"
                    }
}