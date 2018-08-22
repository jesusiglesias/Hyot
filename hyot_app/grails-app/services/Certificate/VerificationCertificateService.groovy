package Certificate

import grails.gorm.transactions.Transactional
import javax.net.ssl.HostnameVerifier
import javax.net.ssl.HttpsURLConnection
import javax.net.ssl.SSLContext
import javax.net.ssl.X509TrustManager

/**
 * Service that contains some utilities for the tasks about requests.
 */
@Transactional
class VerificationCertificateService {

    /**
     * Skips the validation of the certificate in the requests to the Blockchain. This validation fails when the
     * certificate is self-signed.
     */
    def skipValidation() {
        log.debug("VerificationCertificatesService:skipValidation()")

        def nullTrustManager = [
                checkClientTrusted: { chain, authType ->  },
                checkServerTrusted: { chain, authType ->  },
                getAcceptedIssuers: { null }
        ]

        def nullHostnameVerifier = [
                verify: { hostname, session -> true }
        ]

        SSLContext sc = SSLContext.getInstance("SSL")
        sc.init(null, [nullTrustManager as  X509TrustManager] as  X509TrustManager[], null)
        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())
        HttpsURLConnection.setDefaultHostnameVerifier(nullHostnameVerifier as HostnameVerifier)
    }
}
