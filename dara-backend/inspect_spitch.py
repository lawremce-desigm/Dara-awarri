import spitch
import inspect

print("Dir of spitch:")
print(dir(spitch))

if hasattr(spitch, 'Spitch'):
    print("\nHelp on Spitch class:")
    # print(help(spitch.Spitch))
    print(dir(spitch.Spitch))
    
    try:
        client = spitch.Spitch(api_key="test")
        
        print("\nclient.speech.generate signature:")
        print(inspect.signature(client.speech.generate))
        
        print("\nChecking for voices:")
        if hasattr(client, 'voices'):
            print("client.voices found")
            print(dir(client.voices))
        else:
            print("No client.voices found")
            
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No Spitch class found.")
