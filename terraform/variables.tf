variable "prefix" {
    type = "string"
    default = "jodelacpy"
}

variable "location" {
    type = "string"
    default = "eastus"
}

variable "environment" {
    type = "string"
    default = "testing"
}

variable "functionapp" {
    type = "string"
    default = "../build/functionapp.zip"
}

resource "random_string" "storage_name" {
    length = 24
    upper = false
    lower = true
    number = true
    special = false
}