#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Bertrand256
# Created on: 2017-03
from hw_common import HardwareWalletPinException
import logging

def connect_hw(hw_type, ask_for_pin_fun, ask_for_pass_fun):
    try:
        if hw_type == 'TREZOR':
            import hw_intf_trezor as trezor
            import trezorlib.client as client
            try:
                return trezor.connect_trezor(ask_for_pin_fun, ask_for_pass_fun)
            except client.PinException as e:
                raise HardwareWalletPinException(e.args[1])
        elif hw_type == 'KEEPKEY':
            import hw_intf_keepkey as keepkey
            import keepkeylib.client as client
            try:
                return keepkey.connect_keepkey(ask_for_pin_fun, ask_for_pass_fun)
            except client.PinException as e:
                raise HardwareWalletPinException(e.args[1])
        else:
            logging.error('Unsupported HW type: ' + str(hw_type))
    except:
        logging.exception('Exception occurred')


def reconnect_hw(hw_type, client, ask_for_pin_fun, ask_for_pass_fun):
    if hw_type == 'TREZOR':
        from hw_intf_trezor import reconnect_trezor
        return reconnect_trezor(client, ask_for_pin_fun, ask_for_pass_fun)
    elif hw_type == 'KEEPKEY':
        from hw_intf_keepkey import reconnect_keepkey
        return reconnect_keepkey(client, ask_for_pin_fun, ask_for_pass_fun)
    else:
        logging.error('Unsupported HW type: ' + str(hw_type))


def hw_get_address(client, address_n):
    return client.get_address('Dash', address_n, False)


def disconnect_hw(client):
    try:
        client.clear_session()
        client.close()
    except Exception as e:
        pass  # HW must have been disconnected


def prepare_transfer_tx(main_ui, utxos_to_spend, dest_address, tx_fee):
    """
    Creates a signed transaction.
    :param main_ui: Main window for configuration data
    :param utxos_to_spend: list of utxos to send
    :param dest_address: destination (Dash) address
    :param tx_fee: transaction fee
    :return: tuple (serialized tx, total transaction amount in satoshis)
    """
    main_ui.connectHardwareWallet()
    client = main_ui.hw_client
    if client:
        if main_ui.config.hw_type == 'TREZOR':
            import hw_intf_trezor as trezor

            return trezor.prepare_transfer_tx(main_ui, utxos_to_spend, dest_address, tx_fee)

        elif main_ui.config.hw_type == 'KEEPKEY':
            import hw_intf_keepkey as keepkey

            return keepkey.prepare_transfer_tx(main_ui, utxos_to_spend, dest_address, tx_fee)

        else:
            logging.error('Unsupported HW type: ' + str(main_ui.config.hw_type))


def sign_message(main_ui, bip32path, message):
    client = main_ui.hw_client
    if client:
        if main_ui.config.hw_type == 'TREZOR':
            import hw_intf_trezor as trezor

            return trezor.sign_message(main_ui, bip32path, message)

        elif main_ui.config.hw_type == 'KEEPKEY':
            import hw_intf_keepkey as keepkey

            return keepkey.sign_message(main_ui, bip32path, message)

        else:
            logging.error('Unsupported HW type: ' + str(main_ui.config.hw_type))


def change_pin(main_ui, remove=False):
    client = main_ui.hw_client
    if client:
        if main_ui.config.hw_type == 'TREZOR':
            import hw_intf_trezor as trezor

            return trezor.change_pin(main_ui, remove)

        elif main_ui.config.hw_type == 'KEEPKEY':
            import hw_intf_keepkey as keepkey

            return keepkey.change_pin(main_ui, remove)
        else:
            logging.error('Unsupported HW type: ' + str(main_ui.config.hw_type))
