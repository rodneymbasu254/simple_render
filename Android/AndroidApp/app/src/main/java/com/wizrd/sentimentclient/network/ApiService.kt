package com.wizrd.sentimentclient.network

import com.wizrd.sentimentclient.PredictRequest
import com.wizrd.sentimentclient.PredictResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("predict")
    suspend fun predict(
        @Body req: PredictRequest
    ): Response<PredictResponse>
}