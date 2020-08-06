from trajectory_anonymization import *
from sklearn.naive_bayes import CategoricalNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn import tree
from numpy import array, asarray

def separate_traj(trajectories, train_part=0.75):
    train_part = 1 - train_part
    training_set = trajectories[int(len(trajectories) * train_part):]
    test_set = trajectories[:int(len(trajectories) * train_part)]
    return test_set,training_set

def main():
    name = 'dataset_TSMC2014_TKY.csv'
    trajectories = add_duration(split_trajectories(return_dict(name)))
    test_set,training_set = separate_traj(trajectories)
    categories = set()
    for tra in trajectories:
        t = tra.trajectory
        for point in t:
            for cat in point.venue_category_id:
                categories.add(cat)
    categories = list(categories)
    # bayes(test_set,training_set,categories)
    # decisiontree(test_set,training_set,categories)
    # ann(test_set,training_set,categories)
    # similarity_matrix = create_similarity_matrix(trajectories)
    # anon_trajectories = merge_trajectories(trajectories,similarity_matrix,3)
    # test_set,training_set = separate_traj(anon_trajectories)
    # bayes(test_set,training_set,categories)

def decisiontree(test_set,training_set,categories):
    clf = tree.DecisionTreeClassifier()
    x, y = build_xy(training_set, categories)
    clf.fit(x,y)
    # result = clf.predict(x)
    x, y = build_xy(test_set, categories)
    y_predicted = clf.predict(x)
    print(f'score: {clf.score(x, y)}')
    print('tree confusion matrix')
    print(classification_report(x,y_predicted))

def ann(test_set,training_set,categories):
    x, y = build_xy(training_set, categories)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(x,y)
    x, y = build_xy(test_set, categories)
    y_predicted = clf.predict(x)
    print(f'score: {clf.score(x, y)}')
    print('ann confusion matrix')
    print(classification_report(y,y_predicted))

def bayes(test_set,training_set,categories):
    classifier = CategoricalNB()

    x, y = build_xy(training_set, categories)
    classifier.fit(x, y)

    false_positives = 0
    false_negatives = 0
    true_positives = 0
    true_negatives = 0

    x, y = build_xy(test_set, categories)
    y_predicted = classifier.predict(x)
    print(f'score: {classifier.score(x, y)}')
    print('bayes confusion matrix')
    print(classification_report(y,y_predicted))

def copiadepoidistribution(trajectories):
    m = {}
    for trajectory in trajectories:
        for point in trajectory.trajectory:
            for category in point.venue_category_id:
                try:
                    m[category] += 1
                except KeyError:
                    m[category] = 1
    # return m
    m_sum = sum(v for v in m.values())
    return {u: m[u]/m_sum for u in m}

def first(s):
    return next(iter(s))

def build_xy(trajectory_set, categories):
    x = []
    y = []
    for test in trajectory_set:
        trajectory = test.trajectory

        for current, expected in zip(trajectory[:-1], trajectory[1:]):
            x_cats = [categories.index(category) for category in current.venue_category_id]
            y_cats = [categories.index(category) for category in expected.venue_category_id]

            for x_cat in x_cats:
                for y_cat in y_cats:
                    x += [x_cat]
                    y += [y_cat]

    x = asarray(x).reshape(-1,1)
    y = asarray(y)
    return x, y

def counting(trajectories, categories):
    n = {category: {other_category: 0 for other_category in categories}
         for category in categories}
    for trajectory in trajectories:
        compared_category = first(trajectory.trajectory[0].venue_category_id)
        for point in trajectory.trajectory[1:]:
            category = first(point.venue_category_id)
            if compared_category not in n:
                n[compared_category] = {}
            try:
                n[compared_category][category] += 1
            except KeyError:
                n[compared_category][category] = 1
            compared_category = category
    return n

def classifier(n,actual_category):
    return random.choices(list(n[actual_category].keys()), weights=[peso for peso in  n[actual_category].values()])


if __name__ == '__main__':
    main()