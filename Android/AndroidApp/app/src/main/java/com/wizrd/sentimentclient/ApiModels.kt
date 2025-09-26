package com.wizrd.sentimentclient

data class PredictRequest(val text: String)

data class PredictResponse(
    val input: String,
    val prediction: String,
    val score: Double
)