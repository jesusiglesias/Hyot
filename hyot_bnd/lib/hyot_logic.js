/* *********************************************************************************************************************
*                                                                                                                      *
*                                              _    ___     ______ _______                                             *
*                                             | |  | \ \   / / __ \__   __|                                            *
*                                             | |__| |\ \_/ / |  | | | |                                               *
*                                             |  __  | \   /| |  | | | |                                               *
*                                             | |  | |  | | | |__| | | |                                               *
*                                             |_|  |_|  |_|  \____/  |_|                                               *
*                                                                                                                      *
*                   ____            _                         _   _      _                      _                      *
*                  | __ ) _   _ ___(_)_ __   ___  ___ ___    | \ | | ___| |___      _____  _ __| | __                  *
*                  |  _ \| | | / __| | '_ \ / _ \/ __/ __|   |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ /                  *
*                  | |_) | |_| \__ \ | | | |  __/\__ \__ \   | |\  |  __/ |_ \ V  V / (_) | |  |   <                   *
*                  |____/ \__,_|___/_|_| |_|\___||___/___/   |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\                  *
*                                                                                                                      *
*                                                                                                                      *
*        PROJECT:     Hyot                                                                                             *
*           FILE:     hoyt_logic.js                                                                                    *
*                                                                                                                      *
*          USAGE:     ---                                                                                              *
*                                                                                                                      *
*    DESCRIPTION:     Defines the logic of transaction executions using JavaScript                                     *
*                                                                                                                      *
*        OPTIONS:     ---                                                                                              *
*   REQUIREMENTS:     Business network deployed in Hyperledger Fabric                                                  *
*          NOTES:     ---                                                                                              *
*         AUTHOR:     Jesús Iglesias García, jesusgiglesias@gmail.com                                                  *
*   ORGANIZATION:     ---                                                                                              *
*        VERSION:     1.0.0                                                                                            *
*        CREATED:     05/29/18                                                                                         *
*       REVISION:     ---                                                                                              *
*                                                                                                                      *
* *********************************************************************************************************************/

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
