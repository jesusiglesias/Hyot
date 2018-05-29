/************************************************
 *                                              *
 *            HYOT NETWORK DEFINITION           *
 *                                              *
 *        Defines the logic of transaction      *
 *        executions using JavaScript           *
 *                                              *
 ************************************************/

/* global getAssetRegistry getFactory */

'use strict';

/**
 * Publishes a new alert
 * @param {org.hyot.network.PublishAlert} publish_alert The publish_alert transaction
 * @transaction
 */
async function publish(publish_alert) {

    const registry = await getAssetRegistry('org.hyot.network.Alert');
    const factory = getFactory();

    // Creates the alert asset
    const alert_asset = factory.newResource('org.hyot.network', 'Alert', publish_alert.alert_id);
    alert_asset.alert_details = publish_alert.alert_details;

    // Adds the alert asset to the registry
    await registry.add(alert_asset);
}
