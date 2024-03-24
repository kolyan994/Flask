from flask import Flask, jsonify, request
from models import db, Advertisement

app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertisements.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/advertisements', methods=['POST'])
def create_advertisement():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    owner = data.get('owner')

    if not title or not description or not owner:
        return jsonify({'error': 'Missing required fields'}), 400

    new_advertisement = Advertisement(title=title, description=description, owner=owner)
    db.session.add(new_advertisement)
    db.session.commit()

    return jsonify({'message': 'Advertisement created successfully'}), 201


@app.route('/advertisements', methods=['GET'])
def get_all_advertisements():
	advertisements = Advertisement.query.all()
	output = []
	for ad in advertisements:
		ad_data = {'id': ad.id, 'title': ad.title, 'description': ad.description, 'owner': ad.owner}
		output.append(ad_data)
	return jsonify({'advertisements': output})


@app.route('/advertisements/<int:id>', methods=['GET'])
def get_advertisement(id):
	advertisement = Advertisement.query.get_or_404(id)
	return jsonify({'id': advertisement.id, 'title': advertisement.title, 'description': advertisement.description,
					'owner': advertisement.owner})


@app.route('/advertisements/<int:id>', methods=['DELETE'])
def delete_advertisement(id):
	advertisement = Advertisement.query.get_or_404(id)
	db.session.delete(advertisement)
	db.session.commit()
	return jsonify({'message': 'Advertisement deleted successfully'})


@app.route('/advertisements/<int:id>', methods=['PUT'])
def update_advertisement(id):
	advertisement = Advertisement.query.get_or_404(id)
	data = request.get_json()

	if 'title' in data:
		advertisement.title = data['title']
	if 'description' in data:
		advertisement.description = data['description']
	if 'owner' in data:
		advertisement.owner = data['owner']

	db.session.commit()
	return jsonify({'message': 'Advertisement updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)