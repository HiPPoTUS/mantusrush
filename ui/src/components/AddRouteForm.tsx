import React from 'react';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

const AddRouteSchema = Yup.object().shape({
    shipId: Yup.string().required('Required'),
    route: Yup.array().of(Yup.array().of(Yup.number())).required('Required'),
});

const AddRouteForm: React.FC = () => {
    return (
        <Formik
            initialValues={{ shipId: '', route: [] }}
            validationSchema={AddRouteSchema}
            onSubmit={(values) => {
                // Отправка данных на сервер или обновление состояния
            }}
        >
            {({ errors, touched }) => (
                <Form>
                    <Field name="shipId" />
                    {errors.shipId && touched.shipId ? <div>{errors.shipId}</div> : null}
                    <Field name="route" type="hidden" />
                    {errors.route && touched.route ? <div>{errors.route}</div> : null}
                    <button type="submit">Add Route</button>
                </Form>
            )}
        </Formik>
    );
};

export default AddRouteForm;