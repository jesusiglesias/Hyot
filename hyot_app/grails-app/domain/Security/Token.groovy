package Security

/**
 * It represents the general information of the token.
 */
class Token {

    // Attributes
    String token        // Encrypted string
    String tokenType
    String tokenStatus
    Date dateCreated

    // Restrictions on the attributes of the entity
    static constraints = {
        tokenType inList: ['restore']
        tokenStatus defaultValue:false
        dateCreated blank:false
    }
}
