import os
import csv

# Directories and files
data_dir = '.'  # Replace with your dataset directory

# Initialize data structures
users = {}
edges = set()
circles = []
circle_memberships = []
feature_names = []

# Process each ego network
for filename in os.listdir(data_dir):
    if filename.endswith('.egofeat'):
        ego_id = filename.split('.')[0]
        ego_user_id = ego_id  # Use ego ID as userId

        # Load feature names
        featnames_file = os.path.join(data_dir, f'{ego_id}.featnames')
        local_feature_names = []
        with open(featnames_file, 'r') as f:
            for line in f:
                index, name = line.strip().split(' ', 1)
                name = name.replace('anonymized feature ', 'feature_')
                # Remove problematic characters from feature names
                name = name.replace(',', '_').replace(';', '_')
                local_feature_names.append(name)
        # Update global feature names list
        if not feature_names:
            feature_names = local_feature_names

        # Load ego features
        egofeat_file = os.path.join(data_dir, f'{ego_id}.egofeat')
        with open(egofeat_file, 'r') as f:
            features = f.readline().strip().split()
            users[ego_user_id] = {'userId': ego_user_id, 'features': features}

        # Load friends and their features
        feat_file = os.path.join(data_dir, f'{ego_id}.feat')
        with open(feat_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                user_id = parts[0]
                features = parts[1:]
                if user_id not in users:
                    users[user_id] = {'userId': user_id, 'features': features}

        # Load edges
        edges_file = os.path.join(data_dir, f'{ego_id}.edges')
        with open(edges_file, 'r') as f:
            for line in f:
                user1, user2 = line.strip().split()
                # Add edges between friends
                edge = tuple(sorted([user1, user2]))
                edges.add(edge)
                # Add edges between ego and friends
                edges.add(tuple(sorted([ego_user_id, user1])))
                edges.add(tuple(sorted([ego_user_id, user2])))

        # Load circles
        circles_file = os.path.join(data_dir, f'{ego_id}.circles')
        if os.path.exists(circles_file):
            with open(circles_file, 'r') as f:
                circle_counter = 0
                for line in f:
                    parts = line.strip().split()
                    circle_name = parts[0]
                    circle_id = f'{ego_id}_circle_{circle_counter}'
                    circles.append({'circleId': circle_id, 'egoUserId': ego_user_id, 'circleName': circle_name})
                    for user_id in parts[1:]:
                        circle_memberships.append({'userId': user_id, 'circleId': circle_id})
                    circle_counter += 1

# Write users.csv
with open('users.csv', 'w', newline='') as csvfile:
    fieldnames = ['userId:ID(User)'] + feature_names
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(fieldnames)
    num_features = len(feature_names)
    for user in users.values():
        features = user['features']
        # Ensure the features list matches the number of feature names
        if len(features) != num_features:
            # Trim or pad the features list
            features = features[:num_features]
            features += [''] * (num_features - len(features))
        row = [user['userId']] + features
        writer.writerow(row)

# Write edges.csv
with open('edges.csv', 'w', newline='') as csvfile:
    fieldnames = [':START_ID(User)', ':END_ID(User)', ':TYPE']
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(fieldnames)
    for user1, user2 in edges:
        writer.writerow([user1, user2, 'FRIENDS_WITH'])

# Write circles.csv
with open('circles.csv', 'w', newline='') as csvfile:
    fieldnames = ['circleId:ID(Circle)', 'egoUserId', 'circleName']
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(fieldnames)
    for circle in circles:
        writer.writerow([circle['circleId'], circle['egoUserId'], circle['circleName']])

# Write circle_memberships.csv
with open('circle_memberships.csv', 'w', newline='') as csvfile:
    fieldnames = [':START_ID(User)', ':END_ID(Circle)', ':TYPE']
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(fieldnames)
    for membership in circle_memberships:
        writer.writerow([membership['userId'], membership['circleId'], 'IN_CIRCLE'])
