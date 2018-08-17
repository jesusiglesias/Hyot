import grails.util.BuildSettings
import grails.util.Environment
import org.springframework.boot.logging.logback.ColorConverter
import org.springframework.boot.logging.logback.WhitespaceThrowableProxyConverter
import java.nio.charset.Charset

conversionRule 'clr', ColorConverter
conversionRule 'wex', WhitespaceThrowableProxyConverter

// Current environment
Environment current = Environment.getCurrent()

// Instance of ConsoleAppender
// See http://logback.qos.ch/manual/groovy.html for details on configuration
appender('STDOUT', ConsoleAppender) {
    encoder(PatternLayoutEncoder) {
        charset = Charset.forName('UTF-8')

        pattern =
                '%clr(%d{yyyy-MM-dd HH:mm:ss.SSS}){faint} ' +               // Date
                        '%clr(%5p) ' +                                      // Log level
                        '%clr(---){faint} %clr([%15.15t]){faint} ' +        // Thread
                        '%clr(%-40.40logger{39}){cyan} %clr(:){faint} ' +   // Logger
                        '%m%n%wex'                                          // Message
    }
}

// Logger for development or test mode
if (current == Environment.DEVELOPMENT || current == Environment.TEST) {

    logger("hyot_app", DEBUG, ['STDOUT'], false)
    logger("StackTrace", ERROR, ['STDOUT'], false)

    root(ERROR, ['STDOUT'])

// Logger for production mode
} else if (current == Environment.PRODUCTION) {

    def targetDir = BuildSettings.TARGET_DIR

    // Instance of FileAppender
    appender("FULL_STACKTRACE", FileAppender) {
        file = "${targetDir}/stacktrace.log"
        append = true
        encoder(PatternLayoutEncoder) {
            pattern = "%level %logger - %msg%n"
        }
    }
    logger("hyot_app", INFO, ['STDOUT'], false)
    logger("StackTrace", ERROR, ['FULL_STACKTRACE'], false)

    root(ERROR, ['STDOUT'])
}