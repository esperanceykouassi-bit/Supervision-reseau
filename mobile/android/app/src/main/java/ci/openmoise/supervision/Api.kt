package ci.openmoise.supervision

import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import java.util.concurrent.TimeUnit

/**
 * Interface de l'API REST de supervision (consommée par Retrofit).
 * Les trois points d'entrée correspondent aux routes Flask protégées par la
 * clé d'API (en-tête « X-API-Key »).
 */
interface SupervisionApi {
    @GET("api/statistiques")
    suspend fun statistiques(): Statistiques

    @GET("api/equipements")
    suspend fun equipements(): List<Equipement>

    @GET("api/alertes")
    suspend fun alertes(): List<Alerte>
}

/**
 * Fabrique le client Retrofit configuré pour un serveur donné.
 * Un intercepteur OkHttp ajoute automatiquement la clé d'API à chaque requête.
 */
object ApiFactory {
    fun create(baseUrl: String, apiKey: String): SupervisionApi {
        val client = OkHttpClient.Builder()
            .addInterceptor { chain ->
                val requete = chain.request().newBuilder()
                    .addHeader("X-API-Key", apiKey)
                    .build()
                chain.proceed(requete)
            }
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(10, TimeUnit.SECONDS)
            .build()

        val url = if (baseUrl.endsWith("/")) baseUrl else "$baseUrl/"

        return Retrofit.Builder()
            .baseUrl(url)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(SupervisionApi::class.java)
    }
}
