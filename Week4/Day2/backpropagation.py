import tensorflow as tf

x = tf.constant(2.0)
y_true = tf.constant(1.0)

w1 = tf.Variable(0.5)
b1 = tf.Variable(0.3)
w2 = tf.Variable(0.8)
b2 = tf.Variable(0.2)

def sigmoid(z):
    return 1.0 / (1.0 + tf.exp(-z))

with tf.GradientTape() as tape:
    # FORWARD PASS (TF records every op here)
    z1    = w1 * x + b1          # hidden pre-activation
    h     = sigmoid(z1)          # hidden activation
    z2    = w2 * h + b2          # output pre-activation
    y_hat = sigmoid(z2)          # prediction
    loss  = 0.5 * (y_hat - y_true) ** 2  # MSE loss

# BACKWARD PASS = backprop (TF does this for you!)
# tape.gradient() internally runs the chain rule through all 4 steps
grads = tape.gradient(loss, [w1, b1, w2, b2])

# GRADIENT DESCENT UPDATE
lr = 0.1
for var, grad in zip([w1, b1, w2, b2], grads):
    var.assign_sub(lr * grad)

print(f"Updated: w1={w1.numpy():.4f}, b1={b1.numpy():.4f}")
print(f"         w2={w2.numpy():.4f}, b2={b2.numpy():.4f}")