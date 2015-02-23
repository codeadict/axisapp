import logging

from openerp import models, fields

logger = logging.getLogger(__name__)


class MacroChannel(models.Model):
    """
    Base table for macro channel categorization
    """
    _name = "sales.macrochannel"
    _description = "Macro Channel"
    columns = {
        'name': fields.char('Macro Channel'),
    }


class ConsumerOccasion(models.Model):
    """
    Base table for consumer occasion categorization
    """
    _name = "sales.consumer.ocassion"
    _description = "Macro Channel"
    columns = {
        'macro_channel_id': fields.many2one('website', 'Website'),
        'name': fields.char('Macro Channel'),
    }