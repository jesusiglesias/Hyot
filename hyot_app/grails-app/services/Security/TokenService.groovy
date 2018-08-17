package Security

import grails.gorm.transactions.Transactional
import org.jasypt.encryption.pbe.StandardPBEStringEncryptor

/**
 * Service that manages the token.
 */
@Transactional
class TokenService {

    def grailsApplication

    /**
     * It saves the token in database.
     *
     * @param token Token.
     * @return true If token is saved successful in database.
     */
    def save(token) {
        token.save(flush: true, failOnError: true)
    }

    /**
     * It searches the token in database.
     *
     * @param token User's token.
     * @param type Token type.
     * @return true If token exists in database.
     */
    def check_token(token, type){
        return Token.findByTokenAndTokenTypeAndTokenStatus(token, type, false)
    }

    /**
     * It searches the token and modifies its status.
     *
     * @param token Token.
     * @return true If the action is successful.
     */
    def use_token(String token){

        def find_token = Token.findByToken(token)
        find_token.tokenStatus = true

        return find_token.save(flush: true, failOnError: true)
    }

    /**
     * It encrypts the email address.
     *
     * @param email User's email address.
     * @return email Email address encrypted of the user.
     */
    def encrypt(String email){

        // It obtains the configuration
        def jasyptConfig    = grailsApplication.config.jasypt

        def stringEncryptor = new StandardPBEStringEncryptor(jasyptConfig)

        return stringEncryptor.encrypt(email)
    }

    /**
     * It decrypts the email.
     *
     * @param token User's email.
     * @return email Email descrypted of the user.
     */
    def decrypt(String token){
        def jasyptConfig    = grailsApplication.config.jasypt
        def stringEncryptor = new StandardPBEStringEncryptor(jasyptConfig)
        return stringEncryptor.decrypt(token)
    }
}