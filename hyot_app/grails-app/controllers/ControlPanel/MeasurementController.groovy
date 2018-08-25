package ControlPanel

/**
 * It contains actions about measurements for the administrator user.
 */
class MeasurementController {

    def cloudantDBService

    /**
     * It gets all measurements and shows them to the administrator user.
     */
    def getAllMeasurements() {
        log.debug("MeasurementController:getAllMeasurements()")

        def allMeasurements = cloudantDBService.getAllDocs()

        render view: '/controlPanel/measurements', model: [measurements: allMeasurements]
    }
}
