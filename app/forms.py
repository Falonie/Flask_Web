from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        # message = self.errors.get('password')[0]
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()