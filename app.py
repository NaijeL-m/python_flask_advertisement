import flask
from flask import Flask
from flask import request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import sessionmaker
from flask.views import MethodView


app = Flask("app")
Base = declarative_base()
engine = create_engine('postgresql://app:1234@127.0.0.1:5431/netology')
Session = sessionmaker(bind=engine)

class Advert(Base):
    __tablename__ = 'advert'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=False)
    discription = Column(String(512), nullable=False, unique=False)
    owner = Column(String(64), nullable=False, unique=False)
    dateCreate = Column(DateTime, server_default=func.now())

Base.metadata.create_all(engine)
class AdvView(MethodView):
    
    def get(self, adv_id):
        with Session() as session:
            adv = session.query(Advert).get(adv_id)
            return {
                'title': adv.title,
                'discription': adv.discription,
                'owner': adv.owner,
                'dateCreate': adv.dateCreate.isoformat()
            }
    def post(self):
        adv_data = request.json
        with Session() as session:
            new_adv = Advert(title=adv_data['title'], discription=adv_data['discription'], owner=adv_data['owner'])
            session.add(new_adv)
            session.commit()
            return flask.jsonify({'status':'ok', 'id':new_adv.id})

    def patch(self, adv_id):
        adv_data = request.json
        with Session() as session:
            adv = session.query(Advert).get(adv_id)
            for k, v in adv_data.items():
                setattr(adv, k, v)
            session.commit()
        return flask.jsonify({'status': 'ok'})
    def delete(self, adv_id):
        with Session() as session:
            adv = session.query(Advert).get(adv_id)
            session.delete(adv)
            session.commit()
        return flask.jsonify({'status_del': adv.id})

app.add_url_rule('/adverts',view_func=AdvView.as_view('adverts'),methods=['POST','GET'])
app.add_url_rule('/adverts/<int:adv_id>',view_func=AdvView.as_view('advert_get'),methods=['GET','PATCH','DELETE'])
app.run()
