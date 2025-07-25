import yaml
import traceback

def load_model_configs(yaml_file='model_servers.yaml'):
    """
    Load model configurations from a YAML file.
    
    Args:
        yaml_file: Path to the YAML configuration file
        
    Returns:
        Dictionary mapping model shortnames to their configurations
    """
    try:
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Create a dictionary mapping shortnames to full configurations
        models = {}
        for server in config.get('servers', []):
            if 'shortname' in server:
                models[server['shortname']] = server
        
        return models
    except Exception as e:
        print(f"Error loading model configurations: {e}")
        traceback.print_exc()
        return {}

