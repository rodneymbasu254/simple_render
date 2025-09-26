package com.wizrd.sentimentclient

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.lifecycleScope
import com.wizrd.sentimentclient.network.ApiClient
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private val api by lazy { ApiClient.create() }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SentimentApp { text, onResult, onLoading ->
                lifecycleScope.launch {
                    try {
                        onLoading(true)
                        val response = api.predict(PredictRequest(text))
                        if (response.isSuccessful) {
                            val body = response.body()
                            if (body != null) {
                                val label = when (body.prediction) {
                                    "1" -> "Positive"
                                    "0" -> "Negative"
                                    else -> body.prediction
                                }
                                onResult("Prediction: $label\nScore: ${"%.2f".format(body.score)}")
                            } else {
                                onResult("Empty response body")
                            }
                        } else {
                            onResult("Error ${response.code()}: ${response.errorBody()?.string()}")
                        }
                    } catch (e: Exception) {
                        onResult("Request failed: ${e.localizedMessage ?: e.toString()}")
                    } finally {
                        onLoading(false)
                    }
                }
            }
        }
    }
}

@Composable
fun SentimentApp(
    onPredict: (String, (String) -> Unit, (Boolean) -> Unit) -> Unit
) {
    var input by remember { mutableStateOf("") }
    var result by remember { mutableStateOf("Result will appear here") }
    var loading by remember { mutableStateOf(false) }

    Surface(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                label = { Text("Enter text to analyze") },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    if (input.isNotBlank()) {
                        onPredict(
                            input,
                            { res -> result = res },
                            { load -> loading = load }
                        )
                    } else {
                        result = "Please enter some text first."
                    }
                }
            ) {
                Text("Predict")
            }

            Spacer(modifier = Modifier.height(16.dp))

            if (loading) {
                CircularProgressIndicator()
            } else {
                Text(result, modifier = Modifier.fillMaxWidth())
            }
        }
    }
}
